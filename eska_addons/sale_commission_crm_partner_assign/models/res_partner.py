# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    agent = fields.Boolean(string="Agent", compute="_compute_agent", store=True)

    @api.depends('grade_id')
    def _compute_agent(self):
        for record in self:
            record.agent = record.grade_id
