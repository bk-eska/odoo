# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _get_default_number_sequence(self):
        journal = self._search_default_journal()
        return journal.l10n_tr_document_number_sequence

    l10n_tr_document_number_sequence = fields.Many2one(
        comodel_name='ir.sequence',
        string='Number Sequence',
        help='Printed Invoice Number Sequence',
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=_get_default_number_sequence,
    )

    def action_assign_number(self):
        for move in self:
            if move.l10n_tr_document_number_sequence:
                move.l10n_tr_document_number = move.l10n_tr_document_number_sequence.with_context(
                    ir_sequence_date=move.invoice_date,
                    ir_sequence_date_range=move.invoice_date)._next()

    def _post(self, soft=True):
        for move in self.filtered(lambda x: x.l10n_tr_use_document):
            if move.move_type in ['out_invoice', 'in_refund'] and \
                    move.l10n_tr_delivery_type == 'printed' and \
                    move.journal_id.l10n_tr_document_auto_number and \
                    not move.l10n_tr_document_number:
                if not move.l10n_tr_document_number_sequence:
                    move.l10n_tr_document_number_sequence = \
                        move.journal_id.l10n_tr_document_number_sequence
                move.action_assign_number()
        return super()._post(soft)

    @api.onchange('journal_id', 'l10n_tr_delivery_type')
    def _onchange_journal_delivery(self):
        if self.move_type in ['out_invoice', 'in_refund'] and \
                self.l10n_tr_delivery_type == 'printed':
            self.l10n_tr_document_number_sequence = \
                self.journal_id.l10n_tr_document_number_sequence
        else:
            self.l10n_tr_document_number_sequence = False
