# Copyright 2022 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    total_qty = fields.Float(
        string='Total Quantity',
        compute='_compute_total_quantity',
    )

    @api.depends('quant_ids')
    def _compute_total_quantity(self):
        for package in self:
            package.total_qty = sum(package.quant_ids.mapped('quantity'))
