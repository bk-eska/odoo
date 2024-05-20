# Copyright 2021 Eska Technology LLC (www.eskaweb.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CollectionDepositPaymentWizard(models.TransientModel):
    _name = 'collection.deposit.payment.wizard'
    _description = 'Deposit Payment'

    def _default_deposited(self):
        payment_ids = self.env["account.payment"].browse(self._context.get('active_ids', []))
        return sum(payment_ids.mapped('amount'))

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        readonly=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )

    journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Destination Journal',
        required=True,
        domain="[('use_in_collections','!=',True)]",
    )

    destination_payment_method_line_id = fields.Many2one(
        comodel_name='account.payment.method.line',
        string='Destination Payment Method',
        readonly=False,
        store=True,
        copy=False,
        compute='_compute_destination_payment_method_line_id',
        domain="[('id', 'in', available_destination_payment_method_line_ids)]"
    )

    available_destination_payment_method_line_ids = fields.Many2many(
        comodel_name='account.payment.method.line',
        compute='_compute_destination_payment_method_line_fields',
    )

    deposited = fields.Monetary(
        string='Deposit',
        currency_field='currency_id',
        default=_default_deposited,
        readonly=True,
    )

    file = fields.Binary(
        string='Document',
        attachment=True,
    )

    filename = fields.Char()

    @api.depends('available_destination_payment_method_line_ids')
    def _compute_destination_payment_method_line_id(self):
        available_destination_payment_method_lines = self.available_destination_payment_method_line_ids
        if self.destination_payment_method_line_id in available_destination_payment_method_lines:
            self.destination_payment_method_line_id = self.destination_payment_method_line_id
        elif available_destination_payment_method_lines:
            self.destination_payment_method_line_id = \
                available_destination_payment_method_lines[0]._origin
        else:
            self.destination_payment_method_line_id = False

    @api.depends('journal_id')
    def _compute_destination_payment_method_line_fields(self):
        self.available_destination_payment_method_line_ids = self.journal_id._get_available_payment_method_lines('inbound')

    def _create_payment_vals(self, payment):
        collection = payment.collection_line_id.collection_order_id
        payment_method_line_ids = payment.journal_id._get_available_payment_method_lines('outbound')
        if payment.payment_method_line_id.code in ['new_third_party_checks', 'in_third_party_checks']:
            payment_method_line_id = payment_method_line_ids.filtered(lambda l: l.code in ['out_third_party_checks', 'check_printing'])
            check = payment.l10n_latam_check_id or payment
            if check:
                check_number = check.l10n_latam_check_number
                check_payment_date = check.l10n_latam_check_payment_date
                check_bank = check.l10n_latam_check_bank_id.id if check.l10n_latam_check_bank_id else False
                check_issuer_vat = check.l10n_latam_check_issuer_vat
            else:
                check_number = False
                check_payment_date = False
                check_bank = False
                check_issuer_vat = False
        else:
            payment_method_line_id = payment_method_line_ids[0]
            check = False
            check_number = False
            check_payment_date = False
            check_bank = False
            check_issuer_vat = False
        return {
            'date': fields.date.today(),
            'amount': payment.amount,
            'payment_type': 'outbound',
            'payment_method_line_id': payment_method_line_id.id,
            'l10n_latam_check_id': check.id if check else False,
            'l10n_latam_check_number': check_number,
            'l10n_latam_check_payment_date': check_payment_date,
            'l10n_latam_check_bank_id': check_bank,
            'l10n_latam_check_issuer_vat': check_issuer_vat,
            'payment_reference': payment.payment_reference,
            'journal_id': payment.journal_id.id,
            'currency_id': self.currency_id.id,
            'document': self.file,
            'filename': self.filename,
            'collection_id': collection.id,
            'is_internal_transfer': True,
            'destination_journal_id': self.journal_id.id,
            'destination_payment_method_line_id': self.destination_payment_method_line_id.id,
        }

    def deposit_payment(self):
        deposited_payment_ids = []
        payment_ids = self.env["account.payment"].browse(self._context.get('active_ids', []))
        if len(payment_ids.mapped('payment_method_line_id')) > 1:
            raise UserError(_("You may only deposit payments with the same payment method at a time."))
        for payment in payment_ids:
            payment_vals = self._create_payment_vals(payment)
            deposit = self.env['account.payment'].create(payment_vals)
            deposit.sudo().action_post()
            # (payment.move_id + deposit.move_id).line_ids \
            #     .filtered(lambda line: line.account_type == 'asset_receivable') \
            #     .reconcile()
            deposited_payment_ids.append(deposit.id)
        return {
            'name': _('Deposited Payment'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.payment',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', deposited_payment_ids)],
            'context': {
                'create': False,
            },
        }
