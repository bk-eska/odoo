# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResCountryStateCounty(models.Model):
    _inherit = 'res.county'

    better_zip_ids = fields.One2many(
        comodel_name='res.city.zip',
        inverse_name='county_id',
        string='Cities'
    )
