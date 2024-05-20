# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.stock.report.stock_traceability import autoIncrement
from odoo import api, models
from odoo.tools import format_datetime


class MrpStockReport(models.TransientModel):
    _inherit = 'stock.traceability.reports'

    def _make_dict_move(self, level, parent_id, move_line, unfoldable=False):
        res = super(MrpStockReport, self)._make_dict_move(level, parent_id, move_line, unfoldable)
        res[0]['barcode'] = move_line.product_id.barcode
        return res

    @api.model
    def _final_vals_to_lines(self, final_vals, level):
        lines = []
        for data in final_vals:
            lines.append({
                'id': autoIncrement(),
                'model': data['model'],
                'model_id': data['model_id'],
                'parent_id': data['parent_id'],
                'usage': data.get('usage', False),
                'is_used': data.get('is_used', False),
                'lot_name': data.get('lot_name', False),
                'lot_id': data.get('lot_id', False),
                'reference': data.get('reference_id', False),
                'res_id': data.get('res_id', False),
                'res_model': data.get('res_model', False),
                'columns': [data.get('reference_id', False),
                            data.get('product_id', False),
                            data.get('barcode', False),
                            format_datetime(self.env, data.get('date', False), tz=False, dt_format=False),
                            data.get('lot_name', False),
                            data.get('location_source', False),
                            data.get('location_destination', False),
                            data.get('product_qty_uom', 0)],
                'level': level,
                'unfoldable': data['unfoldable'],
            })
        return lines
