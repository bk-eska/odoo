# Copyright 2023 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_return = fields.Boolean(
        string='Is Return',
    )

    def action_confirm(self):
        for order in self.filtered(lambda l: l.is_return):
            for line in order.order_line.filtered(lambda l: l.product_uom_qty > 0):
                line.product_uom_qty *= -1
        return super(SaleOrder, self).action_confirm()
