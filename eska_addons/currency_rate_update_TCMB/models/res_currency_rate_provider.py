# Copyright 2017 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
import pytz
from datetime import datetime, timedelta
from urllib.request import urlopen
from urllib.error import HTTPError
from lxml import etree

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResCurrencyRateProvider(models.Model):
    _inherit = "res.currency.rate.provider"

    service = fields.Selection(
        selection_add=[("TCMB", "Central Bank of the Republic of Turkey")],
        ondelete={"TCMB": "set default"},
    )

    rate_type_ids = fields.One2many(
        comodel_name='res.currency.rate.provider.type',
        inverse_name='provider_id',
        string='Rate Type Mapping',
    )

    def _get_supported_currencies(self):
        self.ensure_one()
        if self.service != "TCMB":
            return super()._get_supported_currencies()  # pragma: no cover
        return [
            "AED", "AUD", "AZN", "BGN", "CAD", "CHF", "CNY", "DKK",
            "EUR", "GBP", "IRR", "JPY", "KRW", "KWD", "NOK", "PKR",
            "QAR", "RON", "RUB", "SAR", "SEK", "USD",
        ]

    def _update(self, date_from, date_to, newest_only=False):
        if self.service != 'TCMB':
            return super()._update(date_from, date_to, newest_only)
        CurrencyRate = self.env["res.currency.rate"]
        is_scheduled = self.env.context.get("scheduled")
        for provider in self:
            try:
                data = provider._obtain_rates(
                    provider.company_id.currency_id.name,
                    provider.currency_ids.mapped("name"),
                    date_from,
                    date_to,
                )
                if data:
                    data = data.items()
            except BaseException as e:
                _logger.warning(
                    'Currency Rate Provider "%(name)s" failed to obtain data since'
                    " %(date_from)s until %(date_to)s"
                    % {
                        "name": provider.name,
                        "date_from": date_from,
                        "date_to": date_to,
                    },
                    exc_info=True,
                )
                provider.message_post(
                    subject=_("Currency Rate Provider Failure"),
                    body=_(
                        'Currency Rate Provider "%(name)s" failed to obtain data'
                        " since %(date_from)s until %(date_to)s:\n%(error)s"
                    )
                         % {
                             "name": provider.name,
                             "date_from": date_from,
                             "date_to": date_to,
                             "error": str(e) if e else _("N/A"),
                         },
                )
                continue

            if not data:
                continue
            if newest_only:
                data = [max(data, key=lambda x: fields.Date.from_string(x[0]))]
            newest_date = False
            for content_date, rates in data:
                timestamp = fields.Date.from_string(content_date)
                if not newest_date or timestamp > newest_date:
                    newest_date = timestamp
                for currency_id, rate_types in rates.items():
                    for rate_type_id, rate in rate_types.items():
                        record = CurrencyRate.search(
                            [
                                ("company_id", "=", provider.company_id.id),
                                ("currency_id", "=", currency_id),
                                ("currency_rate_type_id", "=", rate_type_id),
                                ("name", "=", timestamp),
                            ],
                            limit=1,
                        )
                        if record:
                            record.write({"rate": 1 / rate,
                                          "provider_id": provider.id})
                        else:
                            CurrencyRate.create(
                                {
                                    "company_id": provider.company_id.id,
                                    "currency_id": currency_id,
                                    "currency_rate_type_id": rate_type_id,
                                    "name": timestamp,
                                    "rate": 1 / rate,
                                    "provider_id": provider.id,
                                }
                            )

                if is_scheduled:
                    provider._schedule_last_successful_run(newest_date)
                    provider._schedule_next_run(newest_date)

    def _obtain_rates(self, base_currency, currencies, date_from, date_to):
        self.ensure_one()
        if self.service != "TCMB":
            return super()._obtain_rates(
                base_currency, currencies, date_from, date_to
            )  # pragma: no cover
        if base_currency != "TRY":
            raise UserError(_(
                "TCMB Provider can only be used if base currency is TRY!"))
        content = {}
        day_delta = timedelta(days=1)
        for i in range((date_to - date_from).days + 1):
            dt = date_from + i*day_delta
            content[dt.isoformat()] = self._obtain_tcmb_rates(dt)
        return content

    def _obtain_tcmb_rates(self, dt):
        url = "https://www.tcmb.gov.tr/kurlar/"
        if dt == datetime.now(pytz.timezone('Turkey')).date():
            url = url + "today.xml"
        else:
            pd = dt - timedelta(days=1)
            url = url + pd.strftime("%Y%m/%d%m%Y") + ".xml"
        content = {}
        try:
            with urlopen(url) as response:
                dom = etree.fromstring(response.read())
                for currency in self.currency_ids:
                    content[currency.id] = {}
                    unitxpath = "/Tarih_Date/Currency[@Kod='%s']/Unit/text()" % currency.name
                    for rate in self.rate_type_ids:
                        xpath = "/Tarih_Date/Currency[@Kod='%s']/%s/text()" % \
                                (currency.name, rate.rate_type)
                        rate_type = dom.xpath(xpath, namespaces={})
                        if rate_type:
                            content[currency.id][rate.currency_rate_type_id.id] = float(dom.xpath(xpath, namespaces={})[0]) / float(dom.xpath(unitxpath, namespaces={})[0])
        except HTTPError as e:
            if e.code == 404:
                pass
        return content
