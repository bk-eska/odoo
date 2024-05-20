# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResCurrency(models.Model):
    _inherit = "res.currency"

    def _get_rates(self, company, date):
        if not self.ids:
            return {}
        # Convert False values to None ...
        currency_rate_type = self._context.get('currency_rate_type_id') or None
        # ... and use 'is NULL' instead of '= some-id'.
        operator = '=' if currency_rate_type else 'is'
        self.env['res.currency.rate'].flush_model(
            ['rate', 'currency_id', 'currency_rate_type_id', 'company_id', 'name'])
        query = """SELECT c.id,
                          COALESCE((SELECT r.rate FROM res_currency_rate r
                                  WHERE r.currency_id = c.id AND r.name <= %%s
                                    AND currency_rate_type_id %s %%s
                                    AND (r.company_id IS NULL OR r.company_id = %%s)
                               ORDER BY r.company_id, r.name DESC
                                  LIMIT 1), 1.0) AS rate
                   FROM res_currency c
                   WHERE c.id IN %%s""" % operator
        self._cr.execute(query, (date, currency_rate_type, company.id, tuple(self.ids)))
        currency_rates = dict(self._cr.fetchall())
        return currency_rates

    @api.model
    def _get_conversion_rate(self, from_currency, to_currency, company, date):
        from_rate_type = self._context.get('currency_rate_type_from')
        to_rate_type = self._context.get('currency_rate_type_to')

        if from_rate_type or to_rate_type:
            currency_rates = from_currency.with_context(
                currency_rate_type_id=from_rate_type)._get_rates(company, date)
            from_rate = currency_rates.get(from_currency.id) or 1.0
            currency_rates = to_currency.with_context(
                currency_rate_type_id=to_rate_type)._get_rates(company, date)
            to_rate = currency_rates.get(to_currency.id) or 1.0
            return to_rate / from_rate
        else:
            return super(ResCurrency, self)._get_conversion_rate(
                from_currency, to_currency, company, date)

    def _convert(self, from_amount, to_currency, company, date, round=True):
        self, to_currency = self or to_currency, to_currency or self
        if self == to_currency and \
                self._context.get('currency_rate_type_from') == \
                self._context.get('currency_rate_type_to'):
            to_amount = from_amount
        else:
            to_amount = from_amount * self._get_conversion_rate(
                self, to_currency, company, date)
        return to_currency.round(to_amount) if round else to_amount

    def _select_companies_rates(self):
        return """
            SELECT
                r.currency_id,
                COALESCE(r.company_id, c.id) as company_id,
                r.rate,
                r.name AS date_start,
                (SELECT name FROM res_currency_rate r2
                 WHERE r2.name > r.name AND
                       r2.currency_id = r.currency_id AND
                       r2.currency_rate_type_id IS NULL AND
                       (r2.company_id is null or r2.company_id = c.id)
                 ORDER BY r2.name ASC
                 LIMIT 1) AS date_end
            FROM res_currency_rate r
            JOIN res_company c ON (r.company_id is null or r.company_id = c.id)
            WHERE r.currency_rate_type_id IS NULL
        """

    @api.depends('rate_ids.rate')
    def _compute_current_rate(self):
        from_rate_type = self._context.get('currency_rate_type_from')
        to_rate_type = self._context.get('currency_rate_type_to')

        if from_rate_type:
            self = self.with_context(currency_rate_type_id=from_rate_type)
            return super(ResCurrency, self)._compute_current_rate()
        elif to_rate_type:
            self = self.with_context(currency_rate_type_id=to_rate_type)
            return super(ResCurrency, self)._compute_current_rate()
        else:
            return super(ResCurrency, self)._compute_current_rate()
