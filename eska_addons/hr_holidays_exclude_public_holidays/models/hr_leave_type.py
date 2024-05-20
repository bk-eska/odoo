# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class LeaveType(models.Model):
    _inherit = 'hr.leave.type'

    exclude_public_holidays = fields.Boolean(
        string='Exclude Public Holidays',
    )
