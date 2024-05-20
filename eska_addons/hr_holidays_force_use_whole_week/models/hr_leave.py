# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import timedelta

from odoo import models


class Leave(models.Model):
    _inherit = 'hr.leave'

    def _get_number_of_days(self, date_from, date_to, employee_id):
        if self.holiday_status_id.force_use_whole_week and \
                (date_to - date_from) >= timedelta(days=4):
            if date_to.weekday() == 4:
                date_to += timedelta(days=2)
            elif date_to.weekday() == 5:
                date_to += timedelta(days=1)
        return super(Leave, self)._get_number_of_days(date_from, date_to, employee_id)
