# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    expense_group_id = fields.Many2one(
        comodel_name='account.expense.group',
        string='Expense Group',
        check_company=True,
    )
