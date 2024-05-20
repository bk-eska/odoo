# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    max_leave_count = fields.Integer(
        string='Max Leave Count',
    )

    leave_count_type = fields.Selection(
        selection=[
            ('month', 'Monthly'),
            ('year', 'Yearly'),
        ],
        string='Leave Count Type',
    )
