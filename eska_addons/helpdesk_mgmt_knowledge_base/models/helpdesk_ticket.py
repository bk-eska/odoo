# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    knowledge_base_id = fields.Many2one(
        'helpdesk.ticket.knowledge.base',
        'Solution Description',
    )

    solution = fields.Text(
        string='Solution',
    )

    @api.onchange('knowledge_base_id')
    def _onchange_knowledge_base_id(self):
        self.solution = self.knowledge_base_id.description or False
