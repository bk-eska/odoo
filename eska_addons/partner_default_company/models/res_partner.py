# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _default_company(self):
        if not 'create_company' in self.env.context:
            return self.env.company

    company_id = fields.Many2one(
        default=_default_company
    )
