# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

field_renames = [
    ('account.bank.statement.line', 'account_bank_statement_line', 'use_document', 'l10n_tr_use_document'),
    ('account.journal', 'account_journal', 'use_document', 'l10n_tr_use_document'),
    ('account.journal', 'account_journal', 'payment_subtype', 'l10n_tr_payment_type'),
    ('account.move', 'account_move', 'use_document', 'l10n_tr_use_document'),
    ('account.move', 'account_move', 'invoice_delivery_type', 'l10n_tr_delivery_type'),
    ('account.move', 'account_move', 'delivery_type', 'l10n_tr_delivery_type'),
    ('account.move', 'account_move', 'document_number', 'l10n_tr_document_number'),
    ('account.move', 'account_move', 'document_type', 'l10n_tr_document_type'),
    ('account.move', 'account_move', 'document_type_description', 'l10n_tr_document_type_description'),
    ('account.move', 'account_move', 'document_date', 'l10n_tr_document_date'),
    ('account.move', 'account_move', 'invoice_type', 'l10n_tr_invoice_type'),
    ('account.move', 'account_move', 'payment_subtype', 'l10n_tr_payment_type'),
]

xmlid_deletes = [
    "l10n_tr_base.view_account_journal_form_payment_subtype",
    "l10n_tr_account_document.invoice_tree_einvoice",
    "l10n_tr_account_document.view_account_move_form_document",
    "l10n_tr_account_document.view_account_move_form_payment_subtype",
    "l10n_tr_account_document.view_move_search_document",
    "l10n_tr_account_document.view_account_move_reversal_document",
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
    # projet selection cleanup
    env.cr.execute("DELETE from ir_model_fields_selection "
               "WHERE field_id IN (SELECT id FROM ir_model_fields "
               "WHERE model = 'stock.despatch.queue' and name = 'state')")