# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta
from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    nationality_id = fields.Many2one(
        string="Nationality",
        comodel_name="res.country",
    )

    gender = fields.Selection(
        [("male", "Male"),
         ("female", "Female"),
         ("other", "Other")],
        string="Gender",
    )

    father_name = fields.Char(
        string='Father Name',
    )

    mother_name = fields.Char(
        string='Mother Name',
    )

    maiden_name = fields.Char(
        string='Maiden Name',
    )

    birth_place = fields.Char(
        string='Birth Place',
    )

    birth_date = fields.Date(
        string='Birth Date',
    )
    
    age = fields.Integer(
        string='Age',
        readonly=True,
        compute="_compute_age",
    )

    @api.depends("birth_date")
    def _compute_age(self):
        for record in self:
            age = 0
            if record.birth_date:
                age = relativedelta(fields.Date.today(), record.birth_date).years
            record.age = age
