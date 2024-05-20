# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.product_uom_qty')
    def _compute_total_qty(self):
        for order in self:
            ordered = 0.0
            for line in order.order_line:
                ordered += line.product_uom_qty
            order.update({
                'total_qty_ordered': ordered,
            })

    total_qty_ordered = fields.Float(
        string='Total Ordered Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        store=True,
        readonly=True,
        compute='_compute_total_qty',
    )
