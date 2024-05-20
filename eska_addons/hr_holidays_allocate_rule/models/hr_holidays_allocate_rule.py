from odoo import models, fields
from dateutil.relativedelta import relativedelta


class HrHolidaysAllocateRule(models.Model):
    _name = 'hr.holidays.allocate.rule'
    _description = 'Leave Allocate Rule'
    _order = 'priority desc, name'

    name = fields.Char(
        string='Name',
        required=True,
    )

    active = fields.Boolean(
        string='Active',
        default=True,
    )

    priority = fields.Integer(
        string="Priority",
        required=True,
        default=100,
    )

    category_id = fields.Many2one(
        comodel_name='hr.employee.category',
        string='Tag',
    )

    department_id = fields.Many2one(
        comodel_name='hr.department',
        string='Department',
    )

    job_id = fields.Many2one(
        comodel_name='hr.job',
        string='Job Position',
    )

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
    )

    younger_than = fields.Integer(
        string="Younger Than",
        default=0,
        help='Rule is applied to younger employees than this number if not zero.',
    )

    older_than = fields.Integer(
        string="Older Than",
        default=0,
        help='Rule is applied to older employees than this number if not zero.',
    )

    seniority_years = fields.Integer(
        string="Seniority Years",
        required=True,
        help="Seniority of employee in years."
    )

    leave_type_id = fields.Many2one(
        comodel_name='hr.leave.type',
        required=True,
        string='Leave Type',
        help='Leave type to allocate',
    )

    number_of_days = fields.Float(
        string="Number of Days",
        required=True,
        help="Number of days to allocate."
    )

    auto_approve = fields.Boolean(
        string="Auto Approve"
    )

    def _get_auto_allocate_search_domain(self, employee_id, service_duration_years):
        domain = [
            ('active', '=', True),
            ('seniority_years', '<=', service_duration_years),
            '|',
            ('employee_id', '=', employee_id.id),
            ('employee_id', '=', False),
        ]

        if employee_id.job_id:
            domain.extend([
                '|',
                ('job_id', '=', False),
                ('job_id', '=', employee_id.job_id.id),
            ])
        else:
            domain.extend([
                ('job_id', '=', False),
            ])

        if employee_id.department_id:
            domain.extend([
                '|',
                ('department_id', '=', False),
                ('department_id', '=', employee_id.department_id.id),
            ])
        else:
            domain.extend([
                ('department_id', '=', False),
            ])

        if employee_id.category_ids:
            domain.extend([
                '|',
                ('category_id', '=', False),
                ('category_id', 'in', employee_id.category_ids.ids),
            ])
        else:
            domain.extend([
                ('category_id', '=', False),
            ])

        if employee_id.birthday:
            age = relativedelta(
                fields.Date.from_string(fields.Date.today()),
                fields.Date.from_string(employee_id.birthday)).years
            domain.extend([
                '|',
                '&',
                ('older_than', '=', 0),
                ('younger_than', '>=', age),
                '&',
                ('younger_than', '=', 0),
                ('older_than', '<=', age),
            ])
        else:
            domain.extend([
                ('younger_than', '=', 0),
                ('older_than', '=', 0),
            ])

        return domain

    def allocate_leaves(self):
        employees = self.env['hr.employee'].search([
            ('active', '=', True),
            ('auto_allocate_leave', '=', True),
        ])
        for employee in employees:
            if employee.service_duration_years > 0 and \
                    employee.service_duration_months == 0 and \
                    employee.service_duration_days == 0:
                domain = self._get_auto_allocate_search_domain(
                    employee, employee.service_duration_years)
                rule = self.search(domain, order='priority desc', limit=1)
                if rule:
                    allocation = {
                        'name': rule.name,
                        'employee_ids': [(6, 0, [employee.id])],
                        'holiday_type': 'employee',
                        'number_of_days': rule.number_of_days,
                        'holiday_status_id': rule.leave_type_id.id,
                    }
                    if rule.auto_approve:
                        allocation['state'] = 'validate'
                    self.env['hr.leave.allocation'].create(allocation)
