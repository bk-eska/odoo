# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    origin_country_id = fields.Many2one(
        comodel_name="res.country",
        string="Origin",
        help="Made in ..."
    )
