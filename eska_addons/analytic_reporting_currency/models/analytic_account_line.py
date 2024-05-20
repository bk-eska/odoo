# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    report_currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='company_id.report_currency_id',
    )

    report_currency_amount = fields.Monetary(
        string='RC Amount',
        help="Reporting Currency Amount",
        compute='_compute_reporting_currency_amount',
        store=True,
    )

    @api.depends('company_id.report_currency_id', 'amount')
    def _compute_reporting_currency_amount(self):
        for rec in self:
            rec.report_currency_amount = rec.currency_id._convert(
                rec.amount, rec.report_currency_id,
                rec.company_id, rec.date)
