# Copyright 2023 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

SO_SORTING_CRITERIA = [
    ("name", "By name"),
    ("product_id.name", "By product name"),
    ("product_id.default_code", "By product reference"),
    ("order_id.date_order", "By order date"),
    ("price_unit", "By price"),
    ("product_uom_qty", "By quantity"),
]

SO_SORTING_DIRECTION = [
    ("asc", "Ascending"),
    ("desc", "Descending"),
]


class ResCompany(models.Model):
    _inherit = "res.company"

    default_so_line_order = fields.Selection(
        selection=SO_SORTING_CRITERIA,
        string="Line Order",
        help="Select a sorting criteria for sale order lines.",
    )
    default_so_line_direction = fields.Selection(
        selection=SO_SORTING_DIRECTION,
        string="Sort Direction",
        help="Select a sorting direction for sale order lines.",
    )
