# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountConvertCurrency(models.TransientModel):
    _inherit = 'account.convert.currency'

    def get_default_vals(self, object):
        res = super(AccountConvertCurrency, self).get_default_vals(object)
        res['currency_rate_type_id'] = object.currency_rate_type_id.id
        return res

    def set_move_vals(self, move):
        result = super(AccountConvertCurrency, self).set_move_vals(move)
        if self.currency_rate_method == 'rate_type' and \
                move.currency_id != self.company_currency_id:
            move.currency_rate_type_id = self.currency_rate_type_id
        return result
