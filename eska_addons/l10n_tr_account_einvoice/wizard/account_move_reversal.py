# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    refund_method = fields.Selection(
        selection_add=[
            ('link', 'Link to a Refund E-Invoice'),
        ],
        ondelete={'link': 'cascade'},
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        readonly=True,
    )

    l10n_tr_link_invoice_id = fields.Many2one(
        'account.move',
        string='E-Invoice To Link',
    )

    @api.model
    def default_get(self, fields):
        res = super(AccountMoveReversal, self).default_get(fields)
        move_ids = self.env['account.move'].browse(self.env.context['active_ids']) \
            if self.env.context.get('active_model') == 'account.move' else self.env['account.move']
        if move_ids:
            inv = move_ids[0]
            res['partner_id'] = inv.partner_id.id
            if inv.l10n_tr_delivery_type == 'einvoice' and inv.move_type == 'out_invoice':
                res['refund_method'] = 'link'
                res['date_mode'] = 'entry'
        return res

    def invoice_link(self):
        for inv in self.move_ids:
            if inv.move_type != 'out_invoice':
                raise UserError(_('You can link only customer invoices to refund E-Invoice.'))
            default_values = self._prepare_default_reversal(inv)
            default_values.update({
                'move_type': 'out_refund',
                'reversed_entry_id': inv.id,
            })
            move_vals_list = inv.with_context(active_test=False).copy_data(default_values)[0]
            for e in ['date', 'invoice_date',
                      'l10n_tr_einvoice_sender_id', 'l10n_tr_einvoice_postbox_id',
                      'l10n_tr_einvoice_sequence', 'l10n_tr_einvoice_profile']:
                if e in move_vals_list:
                    move_vals_list.pop(e)
            self.l10n_tr_link_invoice_id.write(move_vals_list)
            subject = _("Invoice refund")
            body = _("%s is linked to this invoice and lines are imported.") % inv.l10n_tr_document_number
            self.l10n_tr_link_invoice_id.message_post(body=body, subject=subject)

        return {
            'name': _('Reverse Moves'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.l10n_tr_link_invoice_id.id,
            'context': {'default_move_type': self.l10n_tr_link_invoice_id.move_type},
        }

    def reverse_moves(self):
        if self.refund_method == 'link':
            return self.invoice_link()
        else:
            return super(AccountMoveReversal, self).reverse_moves()
