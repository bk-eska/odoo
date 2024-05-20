from openupgradelib import openupgrade
from odoo import api, SUPERUSER_ID

module_renames = [
    ('l10n_tr_account_document_stock', 'l10n_tr_stock_document'),
]

field_renames = [
    ('stock.move', 'stock_move', 'document_number', 'l10n_tr_document_number'),
    ('stock.picking', 'stock_picking', 'document_number', 'l10n_tr_document_number'),
    ('stock.picking', 'stock_picking', 'edespatch_delivery_type', 'l10n_tr_document_type'),
    ('stock.picking', 'stock_picking', 'edespatch_date', 'l10n_tr_date_despatch'),
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

def rename_modules(env, module):
    if env["ir.module.module"].search(
            [("name", "=", module[0])]):
        openupgrade.update_module_names(
            env.cr, [(module[0], module[1])], merge_modules=True)

def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for module in module_renames:
        rename_modules(env, module)
    for field in field_renames:
        rename_fields(env, field)

