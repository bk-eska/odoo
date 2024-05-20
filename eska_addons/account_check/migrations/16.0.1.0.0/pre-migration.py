# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

xmlid_renames = [
    (
        "account_check.account_payment_method_new_third_party_checks",
        "l10n_latam_check.account_payment_method_new_third_party_checks",
    ),
    (
        "account_check.account_payment_method_in_third_party_checks",
        "l10n_latam_check.account_payment_method_in_third_party_checks",
    ),
    (
        "account_check.account_payment_method_out_third_party_checks",
        "l10n_latam_check.account_payment_method_out_third_party_checks",
    ),
]
field_renames = [
    ('account.journal', 'account_journal', 'manual_checks',
     'l10n_latam_manual_checks'),
    ('account.journal', 'account_journal', 'use_checkbooks',
     'l10n_latam_manual_checks'),
    ('account.payment', 'account_payment', 'check_id',
     'l10n_latam_check_id'),
    ('account.payment', 'account_payment', 'check_operation_ids',
     'l10n_latam_check_operation_ids'),
    ('account.payment', 'account_payment', 'check_current_journal_id',
     'l10n_latam_check_current_journal_id'),
    ('account.payment', 'account_payment', 'check_warning_msg',
     'l10n_latam_check_warning_msg'),
    ('account.payment', 'account_payment', 'check_number',
     'l10n_latam_check_number'),
    ('account.payment', 'account_payment', 'check_bank_id',
     'l10n_latam_check_bank_id'),
    ('account.payment', 'account_payment', 'check_issuer_vat',
     'l10n_latam_check_issuer_vat'),
    ('account.payment', 'account_payment', 'check_payment_date',
     'l10n_latam_check_payment_date'),
    ('account.payment', 'account_payment', 'manual_checks',
     'l10n_latam_manual_checks'),
    ('account.payment', 'account_payment', 'use_checkbooks',
     'l10n_latam_manual_checks'),
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
    openupgrade.rename_xmlids(env.cr, xmlid_renames)
