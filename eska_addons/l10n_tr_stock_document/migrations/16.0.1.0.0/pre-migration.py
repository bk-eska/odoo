# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

field_renames = [
    ('stock.move', 'stock_move', 'use_document', 'l10n_tr_use_document'),
    ('stock.move', 'stock_move', 'document_number', 'l10n_tr_document_number'),
    ('stock.picking', 'stock_picking', 'use_document', 'l10n_tr_use_document'),
    ('stock.picking', 'stock_picking', 'document_type', 'l10n_tr_document_type'),
    ('stock.picking', 'stock_picking', 'document_number', 'l10n_tr_document_number'),
    ('stock.picking', 'stock_picking', 'date_despatch', 'l10n_tr_date_despatch'),
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
