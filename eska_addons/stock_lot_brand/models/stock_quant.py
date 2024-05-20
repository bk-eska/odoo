# Copyright 2024 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    product_brand_id = fields.Many2one(
        string='Brand',
        comodel_name='product.brand',
        compute='_compute_product_brand',
        store=True,
    )
    
    @api.depends('product_id.product_brand_id', 'lot_id.product_brand_id')
    def _compute_product_brand(self):
        for quant in self:
            if quant.lot_id:
                quant.product_brand_id = quant.lot_id.product_brand_id
            else:
                quant.product_brand_id = quant.product_id.product_brand_id
