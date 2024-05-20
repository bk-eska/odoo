# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models
from odoo.tools import float_compare, float_is_zero


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    def _synchronize_to_moves(self, changed_fields):
        res = super(AccountBankStatementLine, self)._synchronize_to_moves(
            changed_fields)
        for line in self:
            if line.foreign_currency_id:
                real_amount = line.foreign_currency_id._convert(
                    line.amount_currency, line.currency_id,
                    line.company_id, line.date)
                rounding = line.foreign_currency_id.rounding
                if (float_is_zero(line.amount, precision_rounding=rounding)
                        or float_compare(real_amount, line.amount,
                                         precision_rounding=rounding) == 0):
                    line.move_id.write({
                        'currency_rate_method': 'default',
                        'custom_rate': 1.0,
                    })
                else:
                    line.move_id.write({
                        'currency_rate_method': 'fixed_rate',
                        'custom_rate': line.amount_currency / line.amount,
                    })
        return res
