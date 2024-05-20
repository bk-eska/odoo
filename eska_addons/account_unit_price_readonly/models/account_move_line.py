# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    price_unit_editable = fields.Boolean(
        string='Price Unit Editable',
        compute='_compute_price_unit_editable',
    )

    @api.depends('product_id')
    def _compute_price_unit_editable(self):
        for rec in self:
            rec.price_unit_editable = True if self.user_has_groups(
                'account_unit_price_readonly.group_allow_account_unit_price_change') else False
