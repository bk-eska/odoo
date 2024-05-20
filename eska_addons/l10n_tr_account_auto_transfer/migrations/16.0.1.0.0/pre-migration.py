# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

field_renames = [
    ('account.transfer.model', 'account_transfer_model', 'use_account_transfer', 'l10n_tr_use_reflection_account'),
]

xmlid_deletes = [
    "l10n_tr_account_auto_transfer.tr_view_transfer_model_form",
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
    openupgrade.delete_records_safely_by_xml_id(env, xmlid_deletes, True)
    for field in field_renames:
        rename_fields(env, field)
