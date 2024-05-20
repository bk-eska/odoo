# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

xmlid_deletes = [
    "date_range.view_date_range_renumber_form",
    "l10n_tr_account_sequence.view_move_search_sequence",
    "l10n_tr_account_sequence.view_move_line_search_sequence",
]

field_renames = [
    ('account.move', 'account_move', 'move_sequence_number', 'l10n_tr_move_sequence_number'),
    ('account.move.line', 'account_move_line', 'move_sequence_number', 'l10n_tr_move_sequence_number'),
    ('account.move.line', 'account_move_line', 'line_sequence_number', 'l10n_tr_line_sequence_number'),
    ('date.range', 'date_range', 'move_sequence_number_start', 'l10n_tr_move_sequence_number_start'),
    ('date.range', 'date_range', 'move_sequence_number_start', 'l10n_tr_move_sequence_number_start'),
    ('date.range', 'date_range', 'move_sequence_number_stop', 'l10n_tr_move_sequence_number_stop'),
    ('date.range', 'date_range', 'line_sequence_number_start', 'l10n_tr_line_sequence_number_start'),
    ('date.range', 'date_range', 'line_sequence_number_stop', 'l10n_tr_line_sequence_number_stop'),
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
    openupgrade.logged_query(
        env.cr,
        """
        DELETE FROM ir_model_data
        WHERE module = 'date_range'
        AND model = 'date.range.type'
        """,
    )
