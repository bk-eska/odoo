# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = ['account.move', 'currency.rate.mixin']
    _name = 'account.move'

    # set related
    currency_date = fields.Date(
        related='date',
    )

    # rate injected methods
    def _compute_payments_widget_to_reconcile_info(self):
        self = self.with_to_currency()
        return super(AccountMove, self)._compute_payments_widget_to_reconcile_info()

    def _compute_partner_credit_warning(self):
        self = self.with_from_currency()
        return super(AccountMove,self)._compute_partner_credit_warning()

    def _inverse_amount_total(self):
        self = self.with_from_currency()
        return super(AccountMove,self)._inverse_amount_total()

    def _compute_cash_rounding(self, total_amount_currency):
        self = self.with_from_currency()
        return super(AccountMove, self)._compute_cash_rounding()

    def _reverse_moves(self, default_values_list=None, cancel=False):
        return super(AccountMove, self.with_context(exchange=True))._reverse_moves(default_values_list, cancel)