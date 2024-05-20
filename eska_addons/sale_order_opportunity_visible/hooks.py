from openupgradelib import openupgrade
from odoo import api, SUPERUSER_ID


def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    if env["ir.module.module"].search([("name", "=", "sale_show_opportunity")]):
        openupgrade.update_module_names(
            env.cr, [("sale_show_opportunity", "sale_order_opportunity_visible")],
            merge_modules=True
        )
