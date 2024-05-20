# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.onchange("better_zip_id")
    def _onchange_zip_id(self):
        res = super()._onchange_zip_id()
        if self.better_zip_id:
            self.county_id = self.better_zip_id.county_id
        return res
