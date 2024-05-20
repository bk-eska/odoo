# Copyright 2018 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic Account',
        check_company=True,
        groups="hr.group_hr_user",
    )
