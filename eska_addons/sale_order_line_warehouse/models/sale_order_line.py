# Copyright 2022 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='Warehouse', related=False,)

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for rec in res:
            if rec.product_id.warehouse_id:
                rec.warehouse_id = rec.product_id.warehouse_id
            else:
                rec.warehouse_id = rec.order_id.warehouse_id
        return res

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id and self.product_id.warehouse_id:
            self.warehouse_id = self.product_id.warehouse_id
        else:
            self.warehouse_id = self.order_id.warehouse_id

    def _prepare_procurement_values(self, group_id=False):
        vals = super()._prepare_procurement_values(group_id)
        if self.warehouse_id:
            vals.update({
                "warehouse_id": self.warehouse_id,
            })
        return vals
