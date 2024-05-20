# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _order = 'name, variant_sequence, default_code, id'

    variant_sequence = fields.Char(
        string='Variant Sequence',
        compute='_compute_variant_sequence',
        store=True,
        index=True,
    )

    @api.depends('product_template_variant_value_ids.product_attribute_value_id.sequence')
    def _compute_variant_sequence(self):
        for product in self:
            product.variant_sequence = "".join(['{:05d}'.format(v.product_attribute_value_id.sequence) for v in
                                                product.product_template_variant_value_ids])
