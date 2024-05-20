# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    vendor_ids = fields.Many2many(
        comodel_name='res.partner',
        relation="product_categ_vendor_rel",
        string="Vendors",
    )
