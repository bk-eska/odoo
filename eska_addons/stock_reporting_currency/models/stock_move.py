# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from collections import defaultdict
from odoo import fields, models
from odoo.tools import float_is_zero


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_report_currency_price_unit(self):
        self.ensure_one()
        price_unit = self._get_price_unit()
        report_currency_price_unit = self.company_id.currency_id._convert(
            price_unit, self.company_id.report_currency_id,
            self.company_id, fields.Date.context_today(self))
        precision = self.env['decimal.precision'].precision_get('Product Price')
        if self.origin_returned_move_id and self.origin_returned_move_id.sudo().stock_valuation_layer_ids:
            report_currency_price_unit = self.origin_returned_move_id.sudo().stock_valuation_layer_ids[-1].report_currency_unit_cost
        return not float_is_zero(report_currency_price_unit, precision) and report_currency_price_unit or self.product_id.report_currency_standard_price

    def product_price_update_before_done(self, forced_qty=None):
        res = super(StockMove, self).product_price_update_before_done(forced_qty)
        tmpl_dict = defaultdict(lambda: 0.0)
        std_price_update = {}
        for move in self.filtered(lambda move: move._is_in() and move.with_company(move.company_id).product_id.cost_method == 'average'):
            product_tot_qty_available = move.product_id.sudo().with_company(move.company_id).quantity_svl + tmpl_dict[move.product_id.id]
            rounding = move.product_id.uom_id.rounding

            valued_move_lines = move._get_in_move_lines()
            qty_done = 0
            for valued_move_line in valued_move_lines:
                qty_done += valued_move_line.product_uom_id._compute_quantity(valued_move_line.qty_done, move.product_id.uom_id)

            qty = forced_qty or qty_done
            if float_is_zero(product_tot_qty_available, precision_rounding=rounding):
                new_std_price = move._get_report_currency_price_unit()
            elif float_is_zero(product_tot_qty_available + move.product_qty, precision_rounding=rounding) or \
                    float_is_zero(product_tot_qty_available + qty, precision_rounding=rounding):
                new_std_price = move._get_report_currency_price_unit()
            else:
                amount_unit = std_price_update.get((move.company_id.id, move.product_id.id)) or move.product_id.with_company(move.company_id).report_currency_standard_price
                new_std_price = ((amount_unit * product_tot_qty_available) + (move._get_report_currency_price_unit() * qty)) / (product_tot_qty_available + qty)

            tmpl_dict[move.product_id.id] += qty_done
            move.product_id.with_company(move.company_id.id).with_context(disable_auto_svl=True).sudo().write({'report_currency_standard_price': new_std_price})
            std_price_update[move.company_id.id, move.product_id.id] = new_std_price
        for move in self.filtered(lambda move:
                                  move.with_company(move.company_id).product_id.cost_method == 'fifo'
                                  and float_is_zero(move.product_id.sudo().quantity_svl, precision_rounding=move.product_id.uom_id.rounding)):
            move.product_id.with_company(move.company_id.id).sudo().write({'report_currency_standard_price': move._get_report_currency_price_unit()})
        return res
