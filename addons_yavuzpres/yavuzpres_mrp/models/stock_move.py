# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    categ_id = fields.Many2one('product.category', related= 'product_id.categ_id', string='Product Category', readonly=True)

    image_1920 = fields.Binary(string="Image",
                               related="product_id.image_1920")
