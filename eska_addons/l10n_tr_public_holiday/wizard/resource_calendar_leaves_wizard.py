# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class PublicHolidayWizard(models.TransientModel):
    _name = 'resource.calendar.leaves.wizard'
    _description = 'Adds annual holidays to calendar leaves'

    year = fields.Integer(
        string='Year To Add Holidays'
    )

    def action_add_holidays_wizard(self):
        calendars = self.env.context.get('active_ids', [])
        self.env['resource.calendar.leaves'].add_holidays(self.year, calendars)
