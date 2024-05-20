# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_unit_editable = fields.Boolean(
        string='Price Unit Editable',
        compute='_compute_price_unit_editable',
    )

    @api.depends('name')
    def _compute_price_unit_editable(self):
        self.price_unit_editable = True if self.user_has_groups(
            'sale_unit_price_readonly.group_allow_sale_unit_price_change') else False
