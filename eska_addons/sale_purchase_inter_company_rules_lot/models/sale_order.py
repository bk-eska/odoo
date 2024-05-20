# Copyright 2023 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _prepare_purchase_order_line_data(self, so_line, date_order, company):
        res = super(SaleOrder, self)._prepare_purchase_order_line_data(so_line, date_order, company)
        res['lot_id'] = so_line.lot_id and so_line.lot_id.id or False
        return res
