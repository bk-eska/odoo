# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = ['account.payment.register', 'currency.rate.mixin']
    _name = 'account.payment.register'

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

    # override related
    currency_date = fields.Date(
        #string='Date',
        related='payment_date'
    )

    def _create_payment_vals_from_wizard(self, batch_result):
        res = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard(batch_result)
        res['currency_rate_method'] = self.currency_rate_method
        return res
