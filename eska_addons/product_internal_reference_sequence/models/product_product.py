# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model_create_multi
    def create(self, vals_list):
        products = super(ProductProduct, self).create(vals_list)
        for product in products.filtered(lambda l: not l.default_code):
            category = product.categ_id
            if category.internal_reference_seq_id:
                product.default_code = category.internal_reference_seq_id.next_by_id()
