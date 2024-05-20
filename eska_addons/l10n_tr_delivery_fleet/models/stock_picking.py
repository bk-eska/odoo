# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    l10n_tr_vehicle_id = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='Vehicle',
    )

    l10n_tr_trailer_id = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='Trailer',
    )

    @api.onchange("l10n_tr_driver_id")
    def onchange_l10n_tr_driver_id(self):
        if self.l10n_tr_driver_id:
            vehicle = self.env['fleet.vehicle'].search([
                ('driver_id', '=',  self.l10n_tr_driver_id.id),
            ], limit=1)
            if vehicle:
                self.l10n_tr_vehicle_id = vehicle

    @api.onchange("l10n_tr_vehicle_id")
    def onchange_l10n_tr_vehicle_id(self):
        if self.l10n_tr_vehicle_id:
            self.l10n_tr_vehicle_license_plate = self.l10n_tr_vehicle_id.license_plate
            if self.l10n_tr_vehicle_id.driver_id and not self.l10n_tr_driver_id:
                self.l10n_tr_driver_id = self.l10n_tr_vehicle_id.driver_id

    @api.onchange("l10n_tr_trailer_id")
    def onchange_l10n_tr_trailer_id(self):
        if self.l10n_tr_trailer_id:
            self.l10n_tr_trailer_plate_no = self.l10n_tr_trailer_id.license_plate
