# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from holidays import country_holidays
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz


class ResourceCalendarLeave(models.Model):
    _inherit = 'resource.calendar.leaves'

    def add_holidays(self, year=None, calendars=None):
        holidays = country_holidays(country='TR', years=year, language="tr")
        for i, (date, name) in enumerate(holidays.items()):
            if name == "Ramazan Bayramı":
                daybefore = date - timedelta(days=1)
                holidays[datetime(daybefore.year, daybefore.month, daybefore.day)] = name + " Arifesi"
                break

        for i, (date, name) in enumerate(holidays.items()):
            if name == "Kurban Bayramı":
                daybefore = date - timedelta(days=1)
                holidays[datetime(daybefore.year, daybefore.month, daybefore.day)] = name + " Arifesi"
                break

        holidays = zip(holidays.values(), holidays)
        for calendar in calendars:
            for holiday_val, holiday_key in holidays:
                month = holiday_key.month
                day = holiday_key.day
                date_start = datetime(year=year, month=month, day=day, hour=13, minute=0, second=0) - timedelta(days=1)
                date_end = datetime(year=year, month=month, day=day, hour=23, minute=59, second=59) - timedelta(days=1)
                date_from = pytz.timezone('Europe/Istanbul').localize(date_start).astimezone(pytz.utc)
                date_to = pytz.timezone('Europe/Istanbul').localize(date_end).astimezone(pytz.utc)

                leave_vals = {
                    'calendar_id': calendar,
                    'name': holiday_val,
                    'date_from': datetime(date_from.year, date_from.month, day=date_from.day, hour=date_from.hour, minute=date_from.minute, second=date_from.second),
                    'date_to': datetime(date_to.year, date_to.month, day=date_to.day, hour=date_to.hour, minute=date_to.minute, second=date_to.second),
                }

                if self.search(
                        [('date_from', '=', leave_vals['date_from']), ('name', '=', leave_vals['name']),
                         ('calendar_id', '=', leave_vals['calendar_id'])]):
                    continue
                self.create(leave_vals)
        return True

    def cron_add_holidays(self):
        calendars = self.env['resource.calendar'].search([('auto_update', '=', True)]).ids
        self.add_holidays(year=(datetime.now() + relativedelta(years=1)).year, calendars=calendars)
        return True
