# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

field_renames = [
    ('res.company', 'res_company', 'edespatch_enabled', 'l10n_tr_edespatch_enabled'),
    ('res.company', 'res_company', 'edespatch_sender_ids', 'l10n_tr_edespatch_sender_ids'),
    ('res.company', 'res_company', 'edespatch_postbox_ids', 'l10n_tr_edespatch_postbox_ids'),
    ('res.company', 'res_company', 'edespatch_download_registered_user', 'l10n_tr_edespatch_user_download'),
    ('res.company', 'res_company', 'edespatch_registered_user_sequence', 'l10n_tr_edespatch_user_download_sequence'),
    ('res.company', 'res_company', 'edespatch_registered_user_date', 'l10n_tr_edespatch_user_download_date'),
    ('res.partner', 'res_partner', 'edespatch_registered_user', 'l10n_tr_edespatch_user'),
    ('res.partner', 'res_partner', 'edespatch_sender_ids', 'l10n_tr_edespatch_sender_ids'),
    ('res.partner', 'res_partner', 'edespatch_postbox_ids', 'l10n_tr_edespatch_postbox_ids'),
    ('res.partner', 'res_partner', 'default_edespatch_postbox', 'l10n_tr_default_edespatch_postbox'),
    ('stock.picking', 'stock_picking', 'edespatch_uuid', 'l10n_tr_edespatch_uuid'),
    ('stock.picking', 'stock_picking', 'edespatch_envelope_uuid', 'l10n_tr_edespatch_envelope_uuid'),
    ('stock.picking', 'stock_picking', 'edespatch_response_uuid', 'l10n_tr_edespatch_response_uuid'),
    ('stock.picking', 'stock_picking', 'edespatch_state', 'l10n_tr_edespatch_state'),
    ('stock.picking', 'stock_picking', 'edespatch_sender_id', 'l10n_tr_edespatch_sender_id'),
    ('stock.picking', 'stock_picking', 'edespatch_postbox_id', 'l10n_tr_edespatch_postbox_id'),
    ('stock.picking', 'stock_picking', 'edespatch_number_sequence', 'l10n_tr_edespatch_sequence'),
    ('stock.picking', 'stock_picking', 'edespatch_candidate_sender_ids', 'l10n_tr_edespatch_candidate_sender_ids'),
    ('stock.picking', 'stock_picking', 'edespatch_candidate_postbox_ids', 'l10n_tr_edespatch_candidate_postbox_ids'),
    ('stock.picking', 'stock_picking', 'edespatch_zip', 'l10n_tr_edespatch_zip'),
    ('stock.picking.type', 'stock_picking_type', 'edespatch_enabled', 'l10n_tr_edespatch_enabled'),
    ('stock.picking.type', 'stock_picking_type', 'edespatch_sender_id', 'l10n_tr_edespatch_sender_id'),
    ('stock.picking.type', 'stock_picking_type', 'edespatch_number_sequence', 'l10n_tr_edespatch_sequence'),
    ('stock.picking.type', 'stock_picking_type', 'edespatch_postbox_ids', 'l10n_tr_edespatch_postbox_ids'),
    ('stock.picking.return', 'stock_picking.return', 'return_method', 'l10n_tr_return_method'),
    ('stock.picking.return', 'stock_picking.return', 'partner_id', 'l10m_tr_partner_id'),
    ('stock.picking.return', 'stock_picking.return', 'link_picking_id', 'l10n_tr_link_picking_id'),
]

model_renames = [
    ("stock.edespatch.postbox", "l10n_tr.edespatch.postbox"),
    ("stock.edespatch.registered.user", "l10n_tr.edespatch.user"),
    ("stock.edespatch.sender", "l10n_tr.edespatch.sender"),
    ("edespatch.postbox", "l10n_tr.edespatch.postbox"),
    ("edespatch.registered.user", "l10n_tr.edespatch.user"),
    ("edespatch.sender", "l10n_tr.edespatch.sender"),
]

xmlid_deletes = [
    "l10n_tr_stock_edespatch.stock_picking_edespatch_form_inherit",
    "l10n_tr_stock_edespatch.stock_picking_edespatch__document_form_inherit",
    "l10n_tr_stock_edespatch.edespatch_move_search_view",
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
        if openupgrade.column_exists(cr, field[1], field[2]):
            openupgrade.rename_fields(env, [field])

def rename_models(env, model):
    if openupgrade.table_exists(env.cr, model[0].replace('.', '_')) and \
            not openupgrade.table_exists(env.cr, model[1].replace('.', '_')):
        openupgrade.rename_models(env.cr, [(model[0], model[1])])
        openupgrade.rename_tables(env.cr, [(model[0].replace('.', '_'),
                                            model[1].replace('.', '_'))])

@openupgrade.migrate(use_env=True)
def migrate(env, version):
    for field in field_renames:
        rename_fields(env, field)
    for model in model_renames:
        rename_models(env, model)
    openupgrade.delete_records_safely_by_xml_id(env, xmlid_deletes, True)
    # projet selection cleanup
    env.cr.execute("DELETE from ir_model_fields_selection "
               "WHERE field_id IN (SELECT id FROM ir_model_fields "
               "WHERE model = 'stock.despatch.queue' and name = 'state')")
    env.cr.execute("DELETE from ir_model_fields_selection "
               "WHERE field_id IN (SELECT id FROM ir_model_fields "
               "WHERE model = 'edespatch.move' and name = 'state')")
    env.cr.execute("DELETE from ir_model_fields_selection "
               "WHERE field_id IN (SELECT id FROM ir_model_fields "
               "WHERE model = 'edespatch.move' and name = 'edespatch_type')")
    env.cr.execute("DELETE from ir_model_fields_selection "
               "WHERE field_id IN (SELECT id FROM ir_model_fields "
               "WHERE model = 'edespatch.provider' and name = 'environment')")
