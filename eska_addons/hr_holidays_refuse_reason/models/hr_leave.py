# Copyright 2018 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, _


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    def action_refuse(self):
        refuse = self.env.context.get('refuse')
        if not refuse:
            view = self.env.ref('hr_holidays_refuse_reason.hr_leave_refuse_wizard_view_form')
            wiz = self.env['hr.leave.refuse.wizard'].create({'hr_leave_ids': [(4, p.id) for p in self]})
            return {
                'name': _('Refuse Leave Request'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'hr.leave.refuse.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }
        return super().action_refuse()

    def refuse_reason(self, reason):
        for leave in self:
            leave.message_post_with_view(
                'hr_holidays_refuse_reason.hr_leave_template_refuse_reason',
                values={'reason': reason, 'name': leave.name},
                subtype_id=self.env.ref('mail.mt_note').id,
            )
