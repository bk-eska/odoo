# Copyright 2024 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FleetVehicleAssignationLog(models.Model):
    _inherit = 'fleet.vehicle.assignation.log'

    date_start = fields.Datetime(string="Start Date")
    date_end = fields.Datetime(string="End Date")
