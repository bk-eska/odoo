# Copyright 2024 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    otto_order_id = fields.Char(
        string='Otto Order ID',
        readonly=True,
        copy=False,
    )
