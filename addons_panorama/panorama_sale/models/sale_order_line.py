# Copyright 2024 ESKA (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    missing_items = fields.Boolean(
        string='Missing Item',
    )
