# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HelpdeskTicketKnowledgeBase(models.Model):
    _name = "helpdesk.ticket.knowledge.base"

    name = fields.Char(
        string='Solution',
    )

    description = fields.Text(
        string='Description',
    )
