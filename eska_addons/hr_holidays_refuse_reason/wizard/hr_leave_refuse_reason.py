# Copyright 2018 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class HrLeaveRefuseWizard(models.TransientModel):
    _name = "hr.leave.refuse.wizard"
    _description = "Leave refuse Reason wizard"

    reason = fields.Char(string='Reason')
    hr_leave_ids = fields.Many2many('hr.leave')

    def leave_refuse_reason(self):
        self.ensure_one()
        self.with_context(refuse=True).hr_leave_ids.action_refuse()
        self.hr_leave_ids.refuse_reason(self.reason)
        return {'type': 'ir.actions.act_window_close'}


