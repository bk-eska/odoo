# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

field_renames = [
    ('res.company', 'res_company', 'einvoice_enabled', 'l10n_tr_einvoice_enabled'),
    ('res.company', 'res_company', 'einvoice_sender_ids', 'l10n_tr_einvoice_sender_ids'),
    ('res.company', 'res_company', 'einvoice_postbox_ids', 'l10n_tr_einvoice_postbox_ids'),
    ('res.company', 'res_company', 'einvoice_download_registered_user', 'l10n_tr_einvoice_user_download'),
    ('res.company', 'res_company', 'einvoice_registered_user_sequence', 'l10n_tr_einvoice_user_download_sequence'),
    ('res.company', 'res_company', 'einvoice_registered_user_date', 'l10n_tr_einvoice_user_download_date'),
    ('res.company', 'res_company', 'import_incoming_invoice_lines', 'l10n_tr_einvoice_import_invoice_lines'),
    ('res.company', 'res_company', 'earchive_auto_email', 'l10n_tr_earchive_auto_email'),
    ('res.partner', 'res_partner', 'einvoice_registered_user', 'l10n_tr_einvoice_user'),
    ('res.partner', 'res_partner', 'einvoice_sender_ids', 'l10n_tr_einvoice_sender_ids'),
    ('res.partner', 'res_partner', 'einvoice_postbox_ids', 'l10n_tr_einvoice_postbox_ids'),
    ('res.partner', 'res_partner', 'import_incoming_invoice_lines', 'l10n_tr_einvoice_import_invoice_lines'),
    ('res.partner', 'res_partner', 'default_einvoice_profile', 'l10n_tr_default_einvoice_profile'),
    ('res.partner', 'res_partner', 'default_einvoice_postbox', 'l10n_tr_default_einvoice_postbox'),
    ('res.partner.bank', 'res_partner_bank', 'einvoice_sending_enabled', 'l10n_tr_einvoice_send'),
    ('account.journal', 'account_journal', 'einvoice_enabled', 'l10n_tr_einvoice_enabled'),
    ('account.journal', 'account_journal', 'einvoice_postbox_ids', 'l10n_tr_einvoice_postbox_ids'),
    ('account.journal', 'account_journal', 'einvoice_sender_id', 'l10n_tr_einvoice_sender_id'),
    ('account.journal', 'account_journal', 'einvoice_number_sequence', 'l10n_tr_einvoice_sequence'),
    ('account.journal', 'account_journal', 'earchive_number_sequence', 'l10n_tr_earchive_sequence'),
    ('account.journal', 'account_journal', 'branch_id', 'l10n_tr_branch_id'),
    ('account.move', 'account_move', 'delivery_type', 'l10n_tr_delivery_type'),
    ('account.move', 'account_move', 'einvoice_uuid', 'l10n_tr_einvoice_uuid'),
    ('account.move', 'account_move', 'einvoice_envelope_uuid', 'l10n_tr_einvoice_envelope_uuid'),
    ('account.move', 'account_move', 'einvoice_response_uuid', 'l10n_tr_einvoice_response_uuid'),
    ('account.move', 'account_move', 'einvoice_profile', 'l10n_tr_einvoice_profile'),
    ('account.move', 'account_move', 'einvoice_state', 'l10n_tr_einvoice_state'),
    ('account.move', 'account_move', 'einvoice_response_type', 'l10n_tr_einvoice_response_type'),
    ('account.move', 'account_move', 'einvoice_number_sequence', 'l10n_tr_einvoice_sequence'),
    ('account.move', 'account_move', 'einvoice_sender_id', 'l10n_tr_einvoice_sender_id'),
    ('account.move', 'account_move', 'einvoice_postbox_id', 'l10n_tr_einvoice_postbox_id'),
    ('account.move', 'account_move', 'einvoice_number_sequence', 'l10n_tr_einvoice_sequence'),
    ('account.move.reversal', 'account_move_reversal', 'link_invoice_id', 'l10n_tr_link_invoice_id'),
]

model_renames = [
    ("account.einvoice.registered.user", "l10n_tr.einvoice.user"),
    ("account.einvoice.identification", "l10n_tr.party.identification"),
    ("account.einvoice.postbox", "l10n_tr.einvoice.postbox"),
    ("account.einvoice.sender", "l10n_tr.einvoice.sender"),
    ("account.einvoice.user", "l10n_tr.einvoice.user"),
]

xmlid_deletes = [
    "l10n_tr_account_einvoice.view_move_form_document",
    "l10n_tr_account_einvoice.invoice_form_einvoice",
    "l10n_tr_account_einvoice.invoice_tree_einvoice",
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

def rename_models(env, model):
    if openupgrade.table_exists(env.cr, model[0].replace('.', '_')) and \
            not openupgrade.table_exists(env.cr, model[1].replace('.', '_')):
        openupgrade.rename_models(env.cr, [(model[0], model[1])])
        openupgrade.rename_tables(env.cr, [(model[0].replace('.', '_'),
                                            model[1].replace('.', '_'))])

@openupgrade.migrate(use_env=True)
def migrate(env, version):
    openupgrade.delete_records_safely_by_xml_id(env, xmlid_deletes, True)
    for model in model_renames:
        rename_models(env, model)
    for field in field_renames:
        rename_fields(env, field)
