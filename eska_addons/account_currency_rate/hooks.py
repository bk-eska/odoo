from openupgradelib import openupgrade
from odoo import api, SUPERUSER_ID


xmlid_deletes = [
    "account_invoice_currency_rate.view_partner_property_form_currency_rate",
    "base_currency_inverse_rate.view_currency_rate_tree",
    "base_currency_inverse_rate.view_currency_rate_form",
]

module_renames = [
    ('currency_inverse_rate', 'account_currency_rate'),
    ('base_currency_inverse_rate', 'account_currency_rate'),
    ('account_invoice_currency_rate', 'account_currency_rate'),
    ('account_invoice_currency_inverse_rate', 'account_currency_rate'),
]

def rename_modules(env, module):
    if env["ir.module.module"].search(
            [("name", "=", module[0])]):
        openupgrade.update_module_names(
            env.cr, [(module[0], module[1])], merge_modules=True)

def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    openupgrade.delete_records_safely_by_xml_id(env, xmlid_deletes, True)
    for module in module_renames:
        rename_modules(env, module)
