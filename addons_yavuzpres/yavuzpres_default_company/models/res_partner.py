
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _default_company(self):
        if self.env.user.assign_partner_company:
            return self.env.company
        else:
            return False

    company_id = fields.Many2one(
        default=_default_company,
    )
