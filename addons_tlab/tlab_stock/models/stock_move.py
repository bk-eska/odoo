# Copyright 2024 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    x_analitiktag = fields.Char(
        string='Analytic Tag',
        related='invoice_line_ids.analytic_account_ids.display_name',
        store=True,
    )
