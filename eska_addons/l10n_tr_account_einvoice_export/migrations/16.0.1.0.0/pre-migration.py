# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

field_renames = [
    ('account.move', 'account_move', 'einvoice_profile', 'l10n_tr_einvoice_profile'),
    ('account.move', 'account_move', 'einvoice_gtb_refno', 'l10n_tr_einvoice_gtb_refno'),
    ('account.move', 'account_move', 'einvoice_gcb_regno', 'l10n_tr_einvoice_gtb_gcb_tescilno'),
    ('account.move', 'account_move', 'einvoice_gtb_gcb_tescilno', 'l10n_tr_einvoice_gtb_gcb_tescilno'),
    ('account.move', 'account_move', 'einvoice_actual_export_date', 'l10n_tr_einvoice_gtb_export_date'),
    ('account.move', 'account_move', 'einvoice_gtb_export_date', 'l10n_tr_einvoice_gtb_export_date'),
    ('account.move', 'account_move', 'transport_mode_code', 'l10n_tr_transport_mode_code'),
    ('product.template', 'product_template', 'einvoice_shipment_cost', 'l10n_tr_einvoice_shipment_cost'),
    ('product.template', 'product_template', 'einvoice_insurance_cost', 'l10n_tr_einvoice_insurance_cost'),
    ('res.partner', 'res_partner', 'default_einvoice_profile', 'l10n_tr_default_einvoice_profile'),
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
