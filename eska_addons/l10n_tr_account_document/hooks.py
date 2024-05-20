from openupgradelib import openupgrade
from odoo import api, SUPERUSER_ID

module_renames = [
    ('account_invoice_numbering_on_journal', 'l10n_tr_account_document'),
]

def rename_modules(env, module):
    if env["ir.module.module"].search(
            [("name", "=", module[0])]):
        openupgrade.update_module_names(
            env.cr, [(module[0], module[1])], merge_modules=True)

def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for module in module_renames:
        rename_modules(env, module)

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['account.journal'].search([
        ('type', '=', 'sale'),
        ('company_id.country_id.code', '=', 'TR')
    ]).write({'invoice_reference_model': 'tr'})