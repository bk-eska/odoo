# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.depends("zip_id")
    def _compute_county(self):
        if hasattr(super(), "_compute_county"):
            return super()._compute_county()  # pragma: no cover
        for record in self:
            if record.zip_id:
                record.county_id = record.zip_id.county_id
