# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = ['account.payment.register', 'currency.rate.mixin']
    _name = 'account.payment.register'

    def _create_payment_vals_from_wizard(self, batch_result):
        res = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard(batch_result)
        if self.currency_rate_method == 'rate_type':
            res['currency_rate_type_id'] = self.currency_rate_type_id.id
        return res
