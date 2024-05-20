# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    max_leave_limit = fields.Integer(
        string='Maximum Number Of Days Off',
        help='Set to 0 for no limit.'
    )

    min_leave_limit = fields.Integer(
        string='Minimum Number Of Days Off',
        help='Set to 0 for no limit.'
    )
