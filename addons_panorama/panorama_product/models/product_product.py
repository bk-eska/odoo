# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def name_get(self):
        res = super(ProductProduct, self.with_context(display_default_code=False)).name_get()
        return res
