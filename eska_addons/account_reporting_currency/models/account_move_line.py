# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    report_currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='company_id.report_currency_id',
    )

    report_currency_balance = fields.Monetary(
        string='RC Balance',
        currency_field='report_currency_id',
        help="Reporting Currency Balance",
        compute='_compute_report_currency_balance',
        store=True,
    )

    report_currency_credit = fields.Monetary(
        string='RC Credit',
        currency_field='report_currency_id',
        help="Reporting Currency Credit",
        compute='_compute_report_currency_balance',
        store=True,
    )

    report_currency_debit = fields.Monetary(
        string='RC Debit',
        currency_field='report_currency_id',
        help="Reporting Currency Debit",
        compute='_compute_report_currency_balance',
        store=True,
    )

    @api.depends('balance', 'company_currency_id', 'date', 'amount_currency',
                 'company_id.report_currency_id')
    def _compute_report_currency_balance(self):
        for line in self:
            if line.currency_id == line.company_id.report_currency_id:
                line.report_currency_balance = line.amount_currency
                line.report_currency_credit = line.credit
                line.report_currency_debit = line.debit
            else:
                line.report_currency_balance = \
                    line.company_currency_id._convert(
                        line.balance, line.company_id.report_currency_id,
                        line.company_id, line.date)
                line.report_currency_credit = \
                    line.company_currency_id._convert(
                        line.credit, line.company_id.report_currency_id,
                        line.company_id, line.date)
                line.report_currency_debit = \
                    line.company_currency_id._convert(
                        line.debit, line.company_id.report_currency_id,
                        line.company_id, line.date)
