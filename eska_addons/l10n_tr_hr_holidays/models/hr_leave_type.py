# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    leave_reason_id = fields.Many2one(
        comodel_name='hr.leave.reason',
        string='Leave Reason',
    )
