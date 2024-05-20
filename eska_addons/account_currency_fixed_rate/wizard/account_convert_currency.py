# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountConvertCurrency(models.TransientModel):
    _inherit = 'account.convert.currency'

    def get_default_vals(self, object):
        res = super(AccountConvertCurrency, self).get_default_vals(object)
        res['custom_rate'] = object.custom_rate
        res['custom_inverse_rate'] = object.custom_inverse_rate
        return res

    def set_move_vals(self, move):
        result = super(AccountConvertCurrency, self).set_move_vals(move)
        if self.currency_rate_method == 'fixed_rate' and \
                move.currency_id != self.company_currency_id:
            if not self.use_inverse_rate:
                move.custom_rate = self.custom_rate
            else:
                move.custom_inverse_rate = self.custom_inverse_rate
        return result

