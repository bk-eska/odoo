# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class ValidateAccountMove(models.TransientModel):
    _inherit = "validate.account.move"


    def validate_move(self):
        if self._context.get('active_model') == 'account.move':
            domain = [('id', 'in', self._context.get('active_ids', [])),
                      ('state', '=', 'draft')]
        elif self._context.get('active_model') == 'account.journal':
            domain = [('journal_id', '=', self._context.get('active_id')),
                      ('state', '=', 'draft')]
        else:
            raise UserError(_("Missing 'active_model' in context."))

        moves = self.env['account.move'].search(domain).filtered('line_ids')
        if not moves:
            raise UserError(
                _('There are no journal items in the draft state to post.'))
        for move in moves:
            try:
                with self.env.cr.savepoint():
                    move._post(not self.force_post)
            except Exception as e:
                self._cr.rollback()
                msg = _('Batch Validate Error: %s') % str(e)
                move.message_post(body=msg)
            finally:
                self._cr.commit()
        return {'type': 'ir.actions.act_window_close'}