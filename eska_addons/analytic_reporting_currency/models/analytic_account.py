# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from collections import defaultdict


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    report_currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='company_id.report_currency_id',
    )

    report_currency_balance = fields.Monetary(
        string='RC Balance',
        currency_field='report_currency_id',
        help="Reporting Currency Balance",
        compute='_compute_reporting_debit_credit_balance',
    )

    report_currency_debit = fields.Monetary(
        string='RC Debit',
        currency_field='report_currency_id',
        help="Reporting Currency Debit",
        compute='_compute_reporting_debit_credit_balance',
    )

    report_currency_credit = fields.Monetary(
        string='RC Credit',
        currency_field='report_currency_id',
        help="Reporting Currency Credit",
        compute='_compute_reporting_debit_credit_balance',
    )

    @api.depends('line_ids.report_currency_amount')
    def _compute_reporting_debit_credit_balance(self):
        Curr = self.env['res.currency']
        analytic_line_obj = self.env['account.analytic.line']
        domain = [
            ('account_id', 'in', self.ids),
            ('company_id', 'in', [False] + self.env.companies.ids)
        ]
        if self._context.get('from_date', False):
            domain.append(('date', '>=', self._context['from_date']))
        if self._context.get('to_date', False):
            domain.append(('date', '<=', self._context['to_date']))

        user_currency = self.env.company.currency_id
        credit_groups = analytic_line_obj.read_group(
            domain=domain + [('report_currency_amount', '>=', 0.0)],
            fields=['account_id', 'currency_id', 'report_currency_amount'],
            groupby=['account_id', 'currency_id'],
            lazy=False,
        )
        data_credit = defaultdict(float)
        for l in credit_groups:
            data_credit[l['account_id'][0]] += Curr.browse(l['currency_id'][0])._convert(
                l['report_currency_amount'], user_currency, self.env.company, fields.Date.today())

        debit_groups = analytic_line_obj.read_group(
            domain=domain + [('report_currency_amount', '<', 0.0)],
            fields=['account_id', 'currency_id', 'report_currency_amount'],
            groupby=['account_id', 'currency_id'],
            lazy=False,
        )
        data_debit = defaultdict(float)

        for l in debit_groups:
            data_debit[l['account_id'][0]] += Curr.browse(l['currency_id'][0])._convert(
                l['report_currency_amount'], user_currency, self.env.company, fields.Date.today())

        for account in self:
            account.report_currency_debit = abs(data_debit.get(account.id, 0.0))
            account.report_currency_credit = data_credit.get(account.id, 0.0)
            account.report_currency_balance = account.report_currency_credit - account.report_currency_debit
