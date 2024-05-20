from openupgradelib import openupgrade
from odoo import api, SUPERUSER_ID


def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    if env["ir.module.module"].search([("name", "=", "l10n_tr_work_plans")]):
        openupgrade.update_module_names(
            env.cr, [("l10n_tr_work_plans", "l10n_tr_work_schedule")],
            merge_modules=True
        )
