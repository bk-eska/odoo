
from odoo import SUPERUSER_ID, api

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.partner'].search([])._compute_last_order()