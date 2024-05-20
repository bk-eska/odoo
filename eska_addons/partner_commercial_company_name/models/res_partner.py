# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    commercial_name = fields.Char(
        string="Commercial Name",
        help="Commercial name of the company",
    )

    @api.depends('parent_id.is_company',
                 'commercial_partner_id.commercial_name',
                 'commercial_partner_id.name')
    def _compute_commercial_company_name(self):
        for partner in self:
            p = partner.commercial_partner_id
            if p.is_company:
                partner.commercial_company_name = p.commercial_name or p.name
            else:
                partner.commercial_company_name = False

