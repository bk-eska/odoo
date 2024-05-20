# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Leave(models.Model):
    _inherit = 'hr.leave'

    @api.constrains('number_of_days', 'holiday_status_id')
    def check_leave_days(self):
        for leave in self:
            max_limit = leave.holiday_status_id.max_leave_limit
            min_limit = leave.holiday_status_id.min_leave_limit
            if max_limit == min_limit and leave.number_of_days != max_limit > 0:
                raise ValidationError(_('The number of leave days must be %s days for this leave type.' % min_limit))
            elif leave.number_of_days > max_limit > 0:
                raise ValidationError(_('You can request maximum %s leave days for this leave type.' % max_limit))
            elif min_limit > leave.number_of_days > 0:
                raise ValidationError(_('You should request minimum %s leave days for this leave type.' % min_limit))
