# Copyright 2024 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import models, fields, api
from odoo.exceptions import UserError


class MaintenanceEquipmentReturn(models.Model):
    _name = 'maintenance.equipment.return'
    _description = 'Maintenance Equipment Return'

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string="Returner",
        default=lambda self: self.env.user.employee_id,
        required=True,
    )
    equipment_ids = fields.Many2many(
        comodel_name='maintenance.equipment',
        string="Equipments",
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
            ('returned', 'Returned'),
        ],
        string="State",
        default='draft',
    )

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        self.equipment_ids = self.employee_id.equipment_ids

    def action_return(self):
        for equipment in self.equipment_ids:
            if equipment.employee_id != self.employee_id:
                raise UserError("Equipment is not assigned to the current employee.")
            if equipment.employee_id is None:
                raise UserError("Some equipment has already been returned.")
            equipment.employee_id = None
        self.state = 'returned'
