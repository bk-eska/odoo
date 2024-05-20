# Copyright 2024 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand_on_lot = fields.Boolean(
        string='Brand on Lot/Serial',
        help='Select this to use different brands for each lot/serial.',
    )

    brand_invisible = fields.Boolean(
        string='Brand Invisible',
        help='Technical field to hide brand if lot brands are used.',
        related='brand_on_lot',
    )

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if 'product_brand_id' in vals and self.tracking != 'none':
            lots = self.env['stock.lot'].search([
                ('product_id.product_tmpl_id', 'in', self.ids)
            ])
            lots.write({'product_brand_id': vals['product_brand_id']})
        return res