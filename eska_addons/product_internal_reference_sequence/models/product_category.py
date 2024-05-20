# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    internal_reference_seq_id = fields.Many2one(
        comodel_name="ir.sequence",
        string='Internal Reference Sequence',
    )
