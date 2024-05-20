# Copyright 2022 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("warehouse_id")
    def _onchange_warehouse_id(self):
        result = super()._onchange_warehouse_id() or {}
        if "warning" not in result:
            for line in self.order_line:
                if not line.warehouse_id:
                    line.warehouse_id = self.warehouse_id
        return result
