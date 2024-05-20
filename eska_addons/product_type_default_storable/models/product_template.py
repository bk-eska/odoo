# Copyright 2015 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    detailed_type = fields.Selection(
        default='product',
    )
