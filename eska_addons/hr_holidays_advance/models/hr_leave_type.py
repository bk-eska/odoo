# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class HolidaysType(models.Model):
    _inherit = 'hr.leave.type'

    advance_enabled = fields.Boolean(
        string="Advance"
    )
    advance_allowed = fields.Integer(
        string="Allowed Advance",
        default="7",
    )
    advance_start_month = fields.Integer(
        string="Start Month",
        default="6",
    )
    advance_end_month = fields.Integer(
        string="End Month",
        default="12",
    )

    @api.model
    def get_employees_days(self, employee_ids, date=None):
        result = super(HolidaysType, self).get_employees_days(employee_ids, date)
        for employee_id, leave_types in result.items():
            employee = self.env['hr.employee'].sudo().search([('id', '=', employee_id)], limit=1)
            for leave_type_id, days in leave_types.items():
                leave_type = self.env['hr.leave.type'].search([('id', '=', leave_type_id)], limit=1)
                employee_service_duration_months = employee.service_duration_years * 12 + employee.service_duration_months
                if leave_type.advance_enabled and \
                        leave_type.advance_start_month <= employee_service_duration_months < leave_type.advance_end_month:
                    result[employee_id][leave_type_id]['remaining_leaves'] += leave_type.advance_allowed
                    result[employee_id][leave_type_id]['virtual_remaining_leaves'] += leave_type.advance_allowed
                    result[employee_id][leave_type_id]['max_leaves'] += leave_type.advance_allowed
        return result
