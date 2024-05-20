# Copyright 2016 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class SaleReport(models.Model):
    _inherit = "sale.reports"

    reporting_currency_price_total = fields.Float(
        string='RC Total',
        readonly=True
    )

    reporting_currency_price_subtotal = fields.Float(
        string='RC Untaxed Total',
        readonly=True
    )

    reporting_currency_untaxed_amount_to_invoice = fields.Float(
        string='RC Untaxed Amount To Invoice',
        readonly=True
    )

    reporting_currency_untaxed_amount_invoiced = fields.Float(
        string='RC Untaxed Amount Invoiced',
        readonly=True
    )

    reporting_currency_discount_amount = fields.Float(
        string='RC Discount Amount',
        readonly=True
    )

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['reporting_currency_price_total'] = \
            f"""CASE WHEN l.product_id IS NOT NULL THEN SUM(l.price_total / {self._case_value_or_one('s.reporting_currency_currency_rate')} / {self._case_value_or_one('currency_table.rate')}) ELSE 0 END"""
        res['reporting_currency_price_subtotal'] = \
            f"""CASE WHEN l.product_id IS NOT NULL THEN SUM(l.price_subtotal / {self._case_value_or_one('s.reporting_currency_currency_rate')} / {self._case_value_or_one('currency_table.rate')}) ELSE 0 END"""
        res['reporting_currency_untaxed_amount_to_invoice'] = \
            f"""CASE WHEN l.product_id IS NOT NULL THEN SUM(l.untaxed_amount_to_invoice / {self._case_value_or_one('s.reporting_currency_currency_rate')} / {self._case_value_or_one('currency_table.rate')}) ELSE 0 END"""
        res['reporting_currency_untaxed_amount_invoiced'] = \
            f"""CASE WHEN l.product_id IS NOT NULL THEN SUM(l.untaxed_amount_invoiced / {self._case_value_or_one('s.reporting_currency_currency_rate')} / {self._case_value_or_one('currency_table.rate')}) ELSE 0 END"""
        res['reporting_currency_discount_amount'] = \
            f"""CASE WHEN l.product_id IS NOT NULL THEN SUM(l.price_unit * l.product_uom_qty * l.discount / 100.0 / {self._case_value_or_one('s.reporting_currency_currency_rate')} / {self._case_value_or_one('currency_table.rate')}) ELSE 0 END"""
        return res

