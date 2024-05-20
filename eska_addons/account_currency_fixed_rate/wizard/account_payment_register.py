# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountPaymentRegister(models.TransientModel):
    _inherit = ['account.payment.register', 'currency.rate.mixin']
    _name = 'account.payment.register'

    def _create_payment_vals_from_wizard(self, batch_result):
        res = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard(batch_result)
        if self.currency_rate_method == 'fixed_rate':
            res['custom_rate'] = self.custom_rate
            res['custom_inverse_rate'] = self.custom_inverse_rate
        return res
