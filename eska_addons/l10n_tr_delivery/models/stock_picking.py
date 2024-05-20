# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    l10n_tr_weight_additional = fields.Float(
        string='Additional Weight',
        digits='Stock Weight',
        help='Use this field to calculate shipping (gross) weight',
    )

    l10n_tr_number_of_packages = fields.Integer(
        string='Number of Packages',
        copy=False,
        default=1,
    )

    l10n_tr_transporter_id = fields.Many2one(
        comodel_name='res.partner',
        string='Transport Company',
    )

    l10n_tr_driver_id = fields.Many2one(
        comodel_name='res.partner',
        string='Driver',
    )

    l10n_tr_vehicle_license_plate = fields.Char(
        string='Vehicle License Plate',
    )

    l10n_tr_trailer_plate_no = fields.Char(
        string='Trailer Plate No',
    )

    @api.depends('move_line_ids.result_package_id', 'move_line_ids.result_package_id.shipping_weight', 'weight_bulk', 'l10n_tr_weight_additional')
    def _compute_shipping_weight(self):
        super(StockPicking, self)._compute_shipping_weight()
        for picking in self:
            picking.shipping_weight += picking.l10n_tr_weight_additional

    def _put_in_pack(self, move_line_ids, create_package_level=True):
        res = super(StockPicking, self)._put_in_pack(move_line_ids, create_package_level)
        for picking in self:
            picking.l10n_tr_number_of_packages = len(picking.package_ids)
        return res
