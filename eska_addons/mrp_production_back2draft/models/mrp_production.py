# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_back_to_draft(self):
        for rec in self:
            if rec.state == 'cancel':
                rec.state = False
                move_raw_ids = rec.mapped("move_raw_ids").filtered(
                    lambda l: l.state == 'cancel')
                move_raw_ids.action_back_to_draft()
                move_finished_ids = rec.mapped("move_finished_ids").filtered(
                    lambda l: l.state == 'cancel')
                move_finished_ids.action_back_to_draft()
