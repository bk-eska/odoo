# Copyright 2023 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    so_line_order_default = fields.Selection(
        related="company_id.default_so_line_order",
        string="Line Order",
        readonly=False,
    )
    so_line_direction_default = fields.Selection(
        related="company_id.default_so_line_direction",
        string="Sort Direction",
        readonly=False,
    )

    @api.onchange("so_line_order_default")
    def onchange_so_line_order_default(self):
        if not self.so_line_order_default:
            self.so_line_direction_default = False
