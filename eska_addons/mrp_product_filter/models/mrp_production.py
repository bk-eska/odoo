# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    product_id = fields.Many2one(
        domain="""[
            ('type', 'in', ['product', 'consu']),
            ('bom_ids', '!=', False),
            ('bom_ids.active', '=', True),
            ('bom_ids.type', '=', 'normal'),
            '|',
                ('company_id', '=', False),
                ('company_id', '=', company_id)
        ]
        """,
    )
