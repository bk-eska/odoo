# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = ['account.payment', 'currency.rate.mixin']
    _name = 'account.payment'

    # add amount company currency
    amount_company_currency = fields.Monetary(
        string='Company Currency Amount',
        compute='_compute_amount_company_currency',
        currency_field='company_currency_id',
    )

    @api.depends(lambda self: self._get_amount_company_currency_fields())
    def _compute_amount_company_currency(self):
        for rec in self:
            currency = rec.with_from_currency().currency_id
            if rec.company_currency_id and currency:
                rec.amount_company_currency = currency._convert(
                    rec.amount, rec.company_currency_id,
                    rec.company_id,
                    rec.currency_date or fields.Date.context_today(self))
            else:
                rec.amount_company_currency = 0.0

    # override
    @api.depends('currency_id', 'company_currency_id', 'payment_type')
    def _compute_use_currency_rate(self):
        for rec in self:
            rec.use_currency_rate = rec.currency_id != \
                                    rec.company_currency_id \
                                    and rec.payment_type != 'transfer'

    use_currency_rate = fields.Boolean(
        compute='_compute_use_currency_rate',
    )

    # rate setting methods
    @api.model
    def with_to_currency(self):
        return self

    @api.model
    def with_from_currency(self):
        return self

    # rate injected methods
    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        self = self.with_from_currency()
        return super(AccountPayment, self)._prepare_move_line_default_vals(
            write_off_line_vals)

    @api.model
    def _get_trigger_fields_to_synchronize(self):
        res = super()._get_trigger_fields_to_synchronize()
        return res + ('currency_rate_method',)
