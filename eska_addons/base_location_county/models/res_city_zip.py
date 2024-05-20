# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ResCityZip(models.Model):
    _inherit = 'res.city.zip'
    _rec_names_search = ["county_id"]

    county_id = fields.Many2one(
        comodel_name='res.county',
        string='County'
    )

    @api.depends(
        'name',
        'city',
        'county_id',
        'state_id',
        'country_id',
    )
    def name_get(self):
        res = []
        for rec in self:
            name = [rec.name, rec.city_id.name]
            if rec.city_id.county_id:
                name.append(rec.city_id.county_id.name)
            if rec.city_id.state_id:
                name.append(rec.city_id.state_id.name)
            if rec.city_id.country_id:
                name.append(rec.city_id.country_id.name)
            res.append((rec.id, ", ".join(name)))
        return res
