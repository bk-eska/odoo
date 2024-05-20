# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    sale_order_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        string="Source Sale Order Line",
        readonly=True,
    )

    sale_order_ref = fields.Char(
        string="Source Sale Order",
        # readonly=True,
    )

    client = fields.Char(
        string='Customer',
    )

    parent_client = fields.Char(
        string='Teknotel Customer',
    )

    parent_client_ref = fields.Char(
        string='Teknotel Customer Purchase No',
    )

    order_client_ref = fields.Char(
        string='Yavuzpres Customer Purchase No',
    )

    date_source_order = fields.Date(
        string='Source Order Date',
    )
