# Copyright 2017 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from calendar import monthrange

from odoo import api, models, _
from odoo.exceptions import ValidationError


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.constrains('holiday_status_id', 'date_from')
    def check_leave_duration(self):
        for leave in self:
            count_type = leave.holiday_status_id.leave_count_type
            max_count = leave.holiday_status_id.max_leave_count
            if count_type and max_count:
                employee_leave_ids = self.search([
                    ('employee_id', '=', leave.employee_id.id),
                    ('holiday_status_id', '=', leave.holiday_status_id.id),
                    ('state', '=', 'validate'),
                ])
                if count_type == 'month':
                    date_from = leave.date_from.replace(day=1)
                    max_day = monthrange(date_from.year, date_from.month)[1]
                    date_to = date_from.replace(day=max_day)
                elif count_type == 'year':
                    date_from = leave.date_from.replace(day=1, month=1)
                    date_to = leave.date_from.replace(day=31, month=12)
                employee_leaves = employee_leave_ids.filtered(
                    lambda l: date_from.date() <= l.date_from.date() <= date_to.date())
                if len(employee_leaves) >= max_count:
                    raise ValidationError(_(
                        "The maximum count for %s leave type in a %s is %s times." %
                        (leave.holiday_status_id.name,
                         _('month') if count_type == 'month' else _('year'),
                         max_count)
                    ))
