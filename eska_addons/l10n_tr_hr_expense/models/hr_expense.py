# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    billing_party = fields.Char(
        string="Billing Party",
    )

    date = fields.Date(
        default=False,
    )
