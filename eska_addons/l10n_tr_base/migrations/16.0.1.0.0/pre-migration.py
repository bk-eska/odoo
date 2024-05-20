# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

module_renames = [
    ('account_fiscal_position_category', 'l10n_tr_base'),
    ('account_fiscal_position_code', 'l10n_tr_base'),
    ('account_fiscal_position_template_extended', 'l10n_tr_base'),
    ('account_journal_payment_subtype', 'l10n_tr_base'),
    ('account_tax_code', 'l10n_tr_base'),
]

field_renames = [
    ('account.fiscal.position', 'account_fiscal_position',
     'code', 'l10n_tr_fp_code'),
    ('account.tax.group', 'account_tax_group',
     'code', 'l10n_tr_tax_code'),
]

xmlid_deletes = [
    "account_journal_payment_subtype.view_account_journal_form_payment_subtype",
    "account_tax_code.view_tax_form",
    "account_fiscal_position_code.view_account_position_form_code",
    "account_fiscal_position_code.view_account_position_tree_code",
    "account_fiscal_position_category.view_account_fiscal_position_category_form",
    "account_fiscal_position_category.view_account_position_form_category",
    "account_fiscal_position_category.view_account_position_tree_code",
    "account_fiscal_position_template_extended.view_account_position_template_form_extended",
    "account_fiscal_position_template_extended.view_account_position_template_tree_template",
]

def rename_modules(env, module):
    if env["ir.module.module"].search(
            [("name", "=", module[0])]):
        openupgrade.update_module_names(
            env.cr, [(module[0], module[1])], merge_modules=True)

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
    for module in module_renames:
        rename_modules(env, module)
    for field in field_renames:
        rename_fields(env, field)

