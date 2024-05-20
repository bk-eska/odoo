# Copyright 2024 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    brand_on_lot = fields.Boolean(
        string='Brand on Lot/Serial',
        related='product_id.brand_on_lot',
    )
