# Copyright 2024 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    amount_to_deliver = fields.Monetary(
        string='Amount to Deliver',
        compute="_compute_amount_to_deliver",
        store=True,
    )

    @api.depends('order_line.qty_to_deliver', 'order_line.discount', 'order_line.price_unit', 'order_line.tax_id')
    def _compute_amount_to_deliver(self):
        for order in self:
            amount_to_deliver = 0.0
            for line in order.order_line:
                tax_results = self.env['account.tax']._compute_taxes([line.with_context(amount_to_deliver=True)._convert_to_tax_base_line_dict()])
                totals = list(tax_results['totals'].values())[0]
                total_amount_to_deliver = totals['amount_tax'] + totals['amount_untaxed']
                amount_to_deliver += total_amount_to_deliver
            order.amount_to_deliver = amount_to_deliver
