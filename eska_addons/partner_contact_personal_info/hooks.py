from openupgradelib import openupgrade
from odoo import api, SUPERUSER_ID


def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    charfield = env["ir.model.fields"].search([
        ("model", "=", "res.partner"),
        ("name", "=", "nationality_id"),
        ("ttype", "=", "char"),
    ])
    if charfield:
        openupgrade.rename_fields(env, [('res.partner', 'res_partner',
                                        'nationality_id', 'nationality_id_x')])
