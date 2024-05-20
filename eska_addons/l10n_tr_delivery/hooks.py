from openupgradelib import openupgrade
from odoo import api, SUPERUSER_ID

xmlid_deletes = [
    "stock_picking_gross_weight.view_picking_withcarrier_out_form_simple_package",
]

def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    if env["ir.module.module"].search(
            [("name", "=", "stock_picking_gross_weight")]):
        openupgrade.delete_records_safely_by_xml_id(env, xmlid_deletes, True)
        openupgrade.update_module_names(
            env.cr, [("stock_picking_gross_weight", "l10n_tr_delivery")],
            merge_modules=True
        )
