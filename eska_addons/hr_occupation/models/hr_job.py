# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.job'

    occupation_id = fields.Many2one(
        comodel_name='hr.occupation',
        string="Occupation",
    )

