# Copyright 2024 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Skill(models.Model):
    _inherit = 'hr.skill'

    education_duration = fields.Integer(
        string='Duration',
    )
    education_place = fields.Char(
        string='Place of Education',
    )
    educator = fields.Char(
        string='Educator',
    )
    evaluation_score = fields.Float(
        string='Evaluation Score',
    )
