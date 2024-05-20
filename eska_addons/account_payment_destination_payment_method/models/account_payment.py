from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

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

    @api.depends('available_destination_payment_method_line_ids')
    def _compute_destination_payment_method_line_id(self):
        for pay in self:
            available_destination_payment_method_lines = pay.available_destination_payment_method_line_ids
            if pay.destination_payment_method_line_id in available_destination_payment_method_lines:
                pay.destination_payment_method_line_id = pay.destination_payment_method_line_id
            elif available_destination_payment_method_lines:
                pay.destination_payment_method_line_id = available_destination_payment_method_lines[0]._origin
            else:
                pay.destination_payment_method_line_id = False

    @api.depends('payment_type', 'destination_journal_id', 'currency_id')
    def _compute_destination_payment_method_line_fields(self):
        for pay in self:
            pay.available_destination_payment_method_line_ids = pay.destination_journal_id._get_available_payment_method_lines(pay.payment_type == 'outbound' and 'inbound' or 'outbound')
            to_exclude = pay._get_payment_method_codes_to_exclude()
            if to_exclude:
                pay.available_destination_payment_method_line_ids = pay.available_destination_payment_method_line_ids.filtered(lambda x: x.code not in to_exclude)

    def _create_paired_internal_transfer_payment(self):
        for rec in self:
            super(AccountPayment, rec.with_context(
                default_payment_method_line_id=rec.destination_payment_method_line_id.id,
            ))._create_paired_internal_transfer_payment()
