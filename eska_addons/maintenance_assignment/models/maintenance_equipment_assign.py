# Copyright 2024 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from odoo.exceptions import UserError


class MaintenanceEquipmentAssign(models.Model):
    _name = 'maintenance.equipment.assign'
    _description = 'Maintenance Equipment Assign'

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string="Deliverer",
        default=lambda self: self.env.user.employee_id,
        required=True,
    )
    equipment_ids = fields.Many2many(
        comodel_name='maintenance.equipment',
        compute='_compute_equipment_ids',
        string="Equipments",
        required=True,
    )
    date = fields.Date(
        string="Date",
        default=fields.Date.context_today
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string="Company",
        default=lambda self: self.env.company,
    )
    description = fields.Char(
        string="Description",
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('assigned', 'Assigned'),
        ],
        string="State",
        default='draft',
    )

    @api.depends('employee_id')
    def _compute_equipment_ids(self):
        for record in self:
            record.equipment_ids = self.env['maintenance.equipment'].search([
                ('employee_id', '!=', None),
                ('employee_id', '=', record.employee_id.id)
            ])
    def action_assign(self):
        for equipment in self.equipment_ids:
            if equipment.employee_id.id not in [self.employee_id.id, False]:
                raise UserError("Some equipment has already been assigned to an employee.")
            equipment.employee_id = self.employee_id
        self.state = 'assigned'

    def action_return_form(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Return Equipments',
            'res_model': 'maintenance.equipment.return',
            'view_type': 'form',
            'view_mode': 'form',
            'context': {
                'default_equipment_ids': [(6, 0, self.equipment_ids.ids)],
                'default_employee_id': self.employee_id.id,
            },
        }