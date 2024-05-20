# Copyright 2024 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    brand_on_lot = fields.Boolean(
        string='Brand on Lot/Serial',
        related='product_id.brand_on_lot',
    )

    lot_brand_id = fields.Many2one(
        string='Brand',
        comodel_name='product.brand',
        help='This is the brand of this lot/serial.',
    )

    def _get_value_production_lot(self):
        res = super()._get_value_production_lot()
        if self.lot_brand_id:
            res.update({
                'product_brand_id': self.lot_brand_id.id,
            })
        return res
