# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

field_renames = [
    ('stock.picking.type', 'account_journal', 'despatch_number_sequence', 'l10n_tr_despatch_number_sequence'),
    ('stock.picking.type', 'account_journal', 'despatch_auto_number', 'l10n_tr_despatch_auto_number'),
    ('stock.picking', 'account_move', 'despatch_number_sequence', 'l10n_tr_despatch_number_sequence'),
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
