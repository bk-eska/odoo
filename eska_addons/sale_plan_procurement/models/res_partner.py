# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    product_categ_ids = fields.Many2many(
        comodel_name='product.category',
        relation="product_categ_vendor_rel",
        string='Product Categories',
    )

    product_template_ids = fields.Many2many(
        comodel_name='product.template',
        relation="product_template_vendor_rel",
        string='Products',
    )
