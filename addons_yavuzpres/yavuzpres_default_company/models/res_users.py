
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    assign_partner_company = fields.Boolean(
        string="Assign Partner Company",
    )
