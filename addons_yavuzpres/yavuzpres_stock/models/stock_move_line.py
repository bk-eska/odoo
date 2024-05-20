# Copyright 2024 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    current_quantity = fields.Float(string='Current Quantity')

    def write(self, vals):
        res = super(StockMoveLine, self).write(vals)
        for record in self:
            if 'date' in vals and vals['date']:
                record.current_quantity = record.product_id.qty_available
        return res