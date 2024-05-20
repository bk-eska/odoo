# Copyright 2024 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = 'stock.lot'

    brand_on_lot = fields.Boolean(
        string='Brand on Lot/Serial',
        related='product_id.brand_on_lot',
    )

    product_brand_id = fields.Many2one(
        string='Brand',
        comodel_name='product.brand',
        compute='_compute_product_brand',
        store=True,
        readonly=False
    )

    @api.depends('product_id.product_brand_id')
    def _compute_product_brand(self):
        for lot in self:
            lot.product_brand_id = lot.product_id.product_brand_id
