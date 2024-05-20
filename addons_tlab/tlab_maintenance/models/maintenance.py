# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models, _


class MaintenanceEquipmentCategory(models.Model):
    _name = 'maintenance.equipment.location'
    _description = 'Maintenance Equipment Location'

    name = fields.Char(
        'Location Name',
        required=True,
        translate=True,
    )

    color = fields.Integer(
        'Color Index',
    )

    note = fields.Text(
        'Comments',
        translate=True,
    )


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    location_id = fields.Many2one(
        'maintenance.equipment.location',
        string='Equipment Location',
        tracking=True,
    )
