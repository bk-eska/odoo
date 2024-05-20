# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tax_office_id = fields.Many2one(
        comodel_name='account.tax.office',
        string='Tax Office',
    )

    @api.model
    def _commercial_fields(self):
        return super()._commercial_fields() + ['tax_office_id']

