# Copyright 2016 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.reports"

    report_currency_price_subtotal = fields.Float(
        string='Reporting Currency Untaxed Total',
        readonly=True,
        groups="base.group_multi_currency",
    )

    report_currency_price_average = fields.Float(
        string='Reporting Currency Average Price',
        readonly=True,
        group_operator="avg",
        groups="base.group_multi_currency",
    )

    @api.model
    def _select(self):
        res = super(AccountInvoiceReport, self)._select()
        res += ''',
                -line.report_currency_balance AS report_currency_price_subtotal,
                -COALESCE(
                   -- Average line price
                   (line.report_currency_balance / NULLIF(line.quantity, 0.0)) * (CASE WHEN move.move_type IN ('in_invoice','out_refund','in_receipt') THEN -1 ELSE 1 END)
                   -- convert to template uom
                   * (NULLIF(COALESCE(uom_line.factor, 1), 0.0) / NULLIF(COALESCE(uom_template.factor, 1), 0.0)),
                   0.0)  AS report_currency_price_average
        '''
        return res
