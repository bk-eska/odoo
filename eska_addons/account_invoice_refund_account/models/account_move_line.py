# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends('display_type', 'company_id')
    def _compute_account_id(self):
        move_ids = self.mapped('move_id')
        move_type = move_ids[0].move_type if move_ids else False
        return super(AccountMoveLine, self.with_context(
            move_type=move_type))._compute_account_id()
