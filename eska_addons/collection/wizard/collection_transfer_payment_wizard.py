# Copyright 2021 Eska Technology LLC (www.eskaweb.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _


class CollectionTransferPaymentWizard(models.TransientModel):
    _name = 'collection.transfer.payment.wizard'
    _description = 'Transfer Payment Wizard'

    def _default_received(self):
        payment_ids = self.env["account.payment"].browse(self._context.get('active_ids', []))
        return sum(payment_ids.mapped('amount'))

    collection_id = fields.Many2one(
        comodel_name='collection.order',
        string='Destination Collection',
        required=True
    )

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        readonly=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )

    received_amount = fields.Monetary(
        string='Received Amount',
        currency_field='currency_id',
        default=_default_received,
        readonly=True,
    )

    def _create_transfer_payment_vals(self, payment):
        collection = payment.collection_line_id.collection_order_id
        payment_method_line_ids = payment.journal_id._get_available_payment_method_lines('outbound')
        dest_payment_method_line_ids = self.collection_id.journal_id._get_available_payment_method_lines('inbound')
        if payment.payment_method_line_id.code in ['new_third_party_checks', 'in_third_party_checks']:
            payment_method_line_id = payment_method_line_ids.filtered(lambda l: l.code == 'out_third_party_checks')
            dest_payment_method_line_id = dest_payment_method_line_ids.filtered(
                lambda l: l.code == 'in_third_party_checks')
            check = payment
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
            dest_payment_method_line_id = dest_payment_method_line_ids[0]
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
            'l10n_latam_check_id': check.id,
            'l10n_latam_check_number': check_number,
            'l10n_latam_check_payment_date': check_payment_date,
            'l10n_latam_check_bank_id': check_bank,
            'l10n_latam_check_issuer_vat': check_issuer_vat,
            'payment_reference': self.collection_id.name,
            'journal_id': payment.journal_id.id,
            'currency_id': self.currency_id.id,
            'transfer_collection_id': collection.id,
            'is_internal_transfer': True,
            'destination_journal_id': self.collection_id.user_id.journal_id.id,
            'destination_payment_method_line_id': dest_payment_method_line_id.id,
        }

    def collection_transfer_payment(self):
        payment_ids = self.env["account.payment"].browse(self._context.get('active_ids', []))
        CollectionLine = self.env['collection.order.line']
        for payment in payment_ids:
            line = CollectionLine.search([
                ('partner_id', '=', payment.collection_line_id.collection_order_id.user_id.partner_id.id),
                ('collection_order_id', '=', self.collection_id.id),
            ], limit=1)
            if not line:
                line = CollectionLine.sudo().create({
                    'partner_id': payment.collection_line_id.collection_order_id.user_id.partner_id.id,
                    'collection_order_id': self.collection_id.id,
                })
            transfer_vals = self._create_transfer_payment_vals(payment)
            transfer_vals.update({
                'collection_line_id': line.id,
            })
            transfer = self.env['account.payment'].sudo().create(transfer_vals)
            transfer.sudo().action_post()
            # (payment.move_id + transfer.move_id).line_ids.filtered(
            #     lambda line: line.account_type == 'asset_receivable').reconcile()
