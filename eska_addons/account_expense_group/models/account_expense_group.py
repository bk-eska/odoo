# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields
from odoo.osv import expression


class AccountExpenseGroup(models.Model):
    _name = 'account.expense.group'
    _description = 'Expense Group'
    _check_company_auto = True
    _rec_names_search = ['name','code']

    name = fields.Char(
        string='Name',
        required=True,
    )

    code = fields.Char(
        string='Code',
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company
    )

    active = fields.Boolean(
        default=True,
    )

    def name_get(self):
        result = []
        for record in self:
            if record.code:
                result.append((record.id, '[' +
                               record.code + '] ' + record.name))
            else:
                result.append((record.id, record.name))
        return result