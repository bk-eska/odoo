# Copyright 2024 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    reporting_currency_currency_rate = fields.Float(
        string="RC Currency Rate",
        compute='_compute_report_currency_rate',
        compute_sudo=True,
        store=True,
        digits=(12, 6),
    )

    @api.depends('currency_rate', 'company_id.report_currency_id', 'date_order')
    def _compute_report_currency_rate(self):
        for order in self:
            if order.currency_id == order.company_id.report_currency_id:
                order.reporting_currency_currency_rate = 1.0
            else:
                order.reporting_currency_currency_rate = \
                    order.company_id.report_currency_id._convert(
                        1.0, order.currency_id,
                        order.company_id, order.date_order)