# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id and self.use_currency_rate and \
                self.currency_rate_method == 'rate_type':
            if self.payment_type == 'inbound':
                self.currency_rate_type_id = \
                    self.partner_id.sale_currency_rate_type_id
            else:
                self.currency_rate_type_id = \
                    self.partner_id.purchase_currency_rate_type_id

    @api.model
    def _get_currency_rate_fields(self):
        return super(AccountPayment,self)._get_currency_rate_fields() \
               + ['currency_rate_type_id']

    @api.model
    def _get_trigger_fields_to_synchronize(self):
        res = super()._get_trigger_fields_to_synchronize()
        return res + ('currency_rate_type_id',)

    # rate setting methods
    @api.model
    def with_to_currency(self):
        if self.currency_rate_method == 'rate_type':
            return self.with_context(
                currency_rate_type_to=self.currency_rate_type_id.id)
        else:
            return super(AccountPayment,self).with_to_currency()

    @api.model
    def with_from_currency(self):
        if self.currency_rate_method == 'rate_type':
            return self.with_context(
                currency_rate_type_from=self.currency_rate_type_id.id)
        else:
            return super(AccountPayment,self).with_from_currency()
