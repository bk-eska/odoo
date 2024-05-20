# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    final_customer_id = fields.Many2one(
        'res.partner',
        string='Final Customer',
        help='The final customer associated with this sale order.'
    )
