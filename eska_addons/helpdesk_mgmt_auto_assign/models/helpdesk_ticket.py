# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for rec in res:
            if not rec.user_id and rec.team_id.alias_user_id:
                rec.user_id = rec.team_id.alias_user_id
        return res
