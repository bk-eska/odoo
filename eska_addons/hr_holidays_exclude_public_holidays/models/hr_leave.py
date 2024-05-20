# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class Leave(models.Model):
    _inherit = 'hr.leave'

    def _get_number_of_days(self, date_from, date_to, employee_id):
        if self.holiday_status_id.exclude_public_holidays:
            number_of_days = date_to - date_from
            return {'days': number_of_days.days, 'hours': number_of_days.seconds / 3600}
        else:
            return super(Leave, self)._get_number_of_days(date_from, date_to, employee_id)
