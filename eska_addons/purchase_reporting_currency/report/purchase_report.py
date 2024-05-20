# Copyright 2024 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseReport(models.Model):
    _inherit = "purchase.reports"

    report_currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Reporting Currency',
        readonly=True,
    )

    reporting_currency_price_total = fields.Float(
        string='RC Total',
        readonly=True,
    )

    reporting_currency_price_average = fields.Float(
        string='RC Average Cost',
        readonly=True,
        group_operator="avg",
    )

    reporting_currency_untaxed_total = fields.Float(
        string='RC Untaxed Total',
        readonly=True,
    )

    def _select(self):
        res = super(PurchaseReport, self)._select()
        res += ", c.report_currency_id" \
               ", sum(l.price_total / COALESCE(po.reporting_currency_currency_rate, 1.0))::decimal(16,2) * currency_table.rate as reporting_currency_price_total" \
               ", (sum(l.product_qty * l.price_unit / COALESCE(po.reporting_currency_currency_rate, 1.0))/NULLIF(sum(l.product_qty/line_uom.factor*product_uom.factor),0.0))::decimal(16,2) * currency_table.rate as reporting_currency_price_average" \
               ", sum(l.price_subtotal / COALESCE(po.reporting_currency_currency_rate, 1.0))::decimal(16,2) * currency_table.rate as reporting_currency_untaxed_total"
        return res

    def _group_by(self):
        extra_groupby = """
            , c.report_currency_id
        """
        return super()._group_by() + extra_groupby
