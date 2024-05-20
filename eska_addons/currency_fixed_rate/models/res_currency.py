# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    @api.model
    def _get_conversion_rate(self, from_currency, to_currency, company, date):
        fixed_rate_to = self._context.get('fixed_rate_to')
        fixed_rate_from = self._context.get('fixed_rate_from')

        if fixed_rate_to and fixed_rate_from:
            return fixed_rate_to / fixed_rate_from
        elif fixed_rate_to:
            currency_rates = from_currency._get_rates(company, date)
            from_rate = currency_rates.get(from_currency.id) or 1.0
            return fixed_rate_to / from_rate
        elif fixed_rate_from:
            currency_rates = to_currency._get_rates(company, date)
            to_rate = currency_rates.get(to_currency.id) or 1.0
            return to_rate / fixed_rate_from
        else:
            return super(ResCurrency, self)._get_conversion_rate(
                from_currency, to_currency, company, date)

    @api.depends('rate_ids.rate')
    def _compute_current_rate(self):
        fixed_rate_to = self._context.get('fixed_rate_to')
        fixed_rate_from = self._context.get('fixed_rate_from')
        company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company

        if fixed_rate_to and fixed_rate_from:
            for currency in self:
                currency.rate = fixed_rate_to / fixed_rate_from
                currency.inverse_rate = 1 / currency.rate
                if currency != company.currency_id:
                    currency.rate_string = '1 %s = %.6f %s' % (company.currency_id.name, currency.rate, currency.name)
                else:
                    currency.rate_string = ''
        elif fixed_rate_to:
            for currency in self:
                currency.rate = fixed_rate_to
                currency.inverse_rate = 1 / currency.rate
                if currency != company.currency_id:
                    currency.rate_string = '1 %s = %.6f %s' % (company.currency_id.name, currency.rate, currency.name)
                else:
                    currency.rate_string = ''
        elif fixed_rate_from:
            for currency in self:
                currency.rate = fixed_rate_from
                currency.inverse_rate = 1 / currency.rate
                if currency != company.currency_id:
                    currency.rate_string = '1 %s = %.6f %s' % (company.currency_id.name, currency.rate, currency.name)
                else:
                    currency.rate_string = ''
        else:
            return super(ResCurrency, self)._compute_current_rate()
