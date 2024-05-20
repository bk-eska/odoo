# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCountry(models.Model):
    _inherit = 'res.country'

    country_group_id = fields.Many2one(
        comodel_name='res.country.group',
        string='Country Group',
    )
