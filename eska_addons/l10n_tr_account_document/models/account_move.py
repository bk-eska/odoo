# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_tr_use_document = fields.Boolean(
        related='company_id.l10n_tr_use_document',
    )

    l10n_tr_delivery_type = fields.Selection(
        selection=[
            ('printed', 'Printed')
        ],
        string='Delivery Type',
        default='printed',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    l10n_tr_document_number = fields.Char(
        string='Document Number',
        index=True,
        copy=False,
        readonly=True,
        states={'draft': [('readonly', False)],
                'open': [('readonly', False)]},
    )

    l10n_tr_document_type = fields.Selection(
        selection=[
            ('check', 'Check'),
            ('invoice', 'Invoice'),
            ('order-customer', 'Customer Order'),
            ('order-vendor', 'Vendor Order'),
            ('voucher', 'Promissory Note'),
            ('shipment', 'Shipment'),
            ('receipt', 'Receipt'),
            ('other', 'Other'),
        ],
        string='Document Type',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    l10n_tr_document_type_description = fields.Char(
        string='Document Type Description',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    l10n_tr_document_date = fields.Date(
        'Document Date',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    l10n_tr_invoice_type = fields.Selection(
        selection=[
            ('invoice', 'Invoice'),
            ('shipment', 'Shipment'),
        ],
        string='Invoice Type',
        readonly=True,
        required=True,
        default='invoice',
        states={'draft': [('readonly', False)]},
    )

    l10n_tr_payment_type = fields.Selection(
        related='journal_id.l10n_tr_payment_type',
        string='Payment Type',
    )

    def _get_move_display_name(self, show_ref=False):
        result = super(AccountMove, self)._get_move_display_name(show_ref)
        if show_ref and self.l10n_tr_document_number:
            result += ' (%s)' % self.l10n_tr_document_number
        return result

    def _get_invoice_reference_tr_invoice(self):
        return self.l10n_tr_document_number

    def _get_invoice_reference_tr_partner(self):
        return self.l10n_tr_document_number

    def _post(self, soft=True):
        for move in self.filtered(lambda x: x.l10n_tr_use_document):
            if move.move_type in ['out_invoice', 'in_invoice',
                                  'out_refund', 'in_refund']:  # invoices
                move.l10n_tr_document_type = move.l10n_tr_invoice_type
                move.l10n_tr_document_type_description = False
            elif move.move_type in ['out_receipt', 'in_receipt']:  # receipts
                move.l10n_tr_document_type = 'other'
                move.l10n_tr_document_type_description = _('Freelance')
            else:  # others
                journal = move.journal_id
                if journal.type in ['bank', 'cash']:  # payments
                    if journal.l10n_tr_payment_type == 'bank':
                        if move.statement_line_id and not move.l10n_tr_document_number:
                            move.l10n_tr_document_type = 'other'
                            move.l10n_tr_document_type_description = _('Bank Statement')
                            move.l10n_tr_document_number = move.statement_line_id.statement_id.name or move.name
                        elif move.l10n_tr_document_number:
                            move.l10n_tr_document_type = 'other'
                            move.l10n_tr_document_type_description = _('Bank Receipt')
                    elif journal.l10n_tr_payment_type in ['cash', 'credit_card']:
                        move.l10n_tr_document_type = 'receipt'
                        if not move.l10n_tr_document_number:
                            move.l10n_tr_document_number = move.name
                    elif journal.l10n_tr_payment_type == 'check':
                        move.l10n_tr_document_type = 'check'
                    elif journal.l10n_tr_payment_type == 'promissory':
                        move.l10n_tr_document_type = 'voucher'
                    elif journal.l10n_tr_payment_type not in \
                            dict(journal.fields_get(allfields=['l10n_tr_payment_type'])
                                 ['l10n_tr_payment_type']['selection']):
                        raise ValidationError(_('Payment type of journal is invalid!'))
            if move.l10n_tr_document_type and not move.l10n_tr_document_number:
                raise ValidationError(_('Please enter document number!'))
            if move.move_type != 'entry':
                if self.env['account.move'].search([
                    ('id', '!=', move.id),
                    ('state', '=', 'posted'),
                    ('move_type', '=', move.move_type),
                    ('l10n_tr_document_number', '=', move.l10n_tr_document_number),
                    ('commercial_partner_id', '=', move.commercial_partner_id.id),
                ]):
                    raise ValidationError(_('Invoice %s is posted before!') % move.l10n_tr_document_number)
        res = super()._post(soft)
        for move in self.filtered(lambda x: x.l10n_tr_use_document):
            if move.l10n_tr_document_type:
                if move.move_type != 'entry':  # invoices
                    move.l10n_tr_document_date = move.invoice_date
                elif journal.type in ['bank', 'cash']:
                    move.l10n_tr_document_date = move.date
                elif not move.l10n_tr_document_date:  # others
                    move.l10n_tr_document_date = move.date
        return res
