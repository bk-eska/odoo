# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def set_partner_rate_type(self):
        if self.partner_id and self.use_currency_rate and \
                self.currency_rate_method == 'rate_type':
            if self.move_type in ['out_invoice', 'out_refund']:
                self.currency_rate_type_id = \
                    self.partner_id.sale_currency_rate_type_id
            elif self.move_type in ['in_invoice', 'in_refund']:
                self.currency_rate_type_id = \
                    self.partner_id.purchase_currency_rate_type_id
        else:
            self.currency_rate_type_id = False

    @api.onchange('partner_id', 'currency_rate_method')
    def _onchange_currency_rate_method(self):
        self.set_partner_rate_type()

    @api.model_create_multi
    def create(self, vals_list):
        moves = super(AccountMove, self).create(vals_list)
        for move in moves:
            if not move.currency_rate_type_id:
                move.set_partner_rate_type()
        return moves

