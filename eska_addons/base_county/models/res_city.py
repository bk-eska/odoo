# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCity(models.Model):
    _inherit = "res.city"

    county_id = fields.Many2one(
        comodel_name='res.county',
        string='County'
    )
