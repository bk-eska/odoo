# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _get_stock_move_values(
            self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        move_values = super()._get_stock_move_values(
            product_id, product_qty, product_uom, location_id, name, origin, company_id, values)
        if values.get('remark'):
            move_values['remark'] = values['remark']
        return move_values

