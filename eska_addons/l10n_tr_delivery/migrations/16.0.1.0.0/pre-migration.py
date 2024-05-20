# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

field_renames = [
    ('res.partner', 'res_partner', 'is_transporter', 'l10n_tr_is_transporter'),
    ('res.partner', 'res_partner', 'is_driver', 'l10n_tr_is_driver'),
    ('stock.picking', 'stock_picking', 'weight_additional', 'l10n_tr_weight_additional'),
    ('stock.picking', 'stock_picking', 'number_of_packages', 'l10n_tr_number_of_packages'),
    ('stock.picking', 'stock_picking', 'edespatch_carrier_id', 'l10n_tr_transporter_id'),
    ('stock.picking', 'stock_picking', 'transporter_id', 'l10n_tr_transporter_id'),
    ('stock.picking', 'stock_picking', 'driver_id', 'l10n_tr_driver_id'),
    ('stock.picking', 'stock_picking', 'vehicle_id', 'l10n_tr_vehicle_license_plate'),
    ('stock.picking', 'stock_picking', 'vehicle_license_plate', 'l10n_tr_vehicle_license_plate'),
    ('stock.picking', 'stock_picking', 'transport_equipment_id', 'l10n_tr_trailer_plate_no'),
    ('stock.picking', 'stock_picking', 'trailer_plate_no', 'l10n_tr_trailer_plate_no'),
]

def rename_fields(env, field):
    cr = env.cr
    cr.execute('SELECT name FROM ir_model_fields WHERE model=%s AND name=%s',
        (field[0], field[3]))
    if cr.fetchall():
        return
    cr.execute('SELECT name FROM ir_model_fields WHERE model=%s AND name=%s',
               (field[0], field[2]))
    if cr.fetchall():
        openupgrade.rename_fields(env, [field])

@openupgrade.migrate(use_env=True)
def migrate(env, version):
    for field in field_renames:
        rename_fields(env, field)
