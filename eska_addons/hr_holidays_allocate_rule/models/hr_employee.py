# Copyright 2024 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    auto_allocate_leave = fields.Boolean(
        string='Auto Allocate Leaves',
        default=True,
        groups="hr.group_hr_user",
    )