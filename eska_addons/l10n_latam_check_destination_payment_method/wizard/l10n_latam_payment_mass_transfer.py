from odoo import api, fields, models


class L10nLatamPaymentMassTransfer(models.TransientModel):
    _inherit = 'l10n_latam.payment.mass.transfer'

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
                pay.destination_payment_method_line_id = \
                available_destination_payment_method_lines[0]._origin
            else:
                pay.destination_payment_method_line_id = False

    @api.depends('destination_journal_id')
    def _compute_destination_payment_method_line_fields(self):
        for pay in self:
            pay.available_destination_payment_method_line_ids = pay.destination_journal_id._get_available_payment_method_lines('inbound')

    def _create_payments(self):
        return super(L10nLatamPaymentMassTransfer, self.with_context(
            default_destination_payment_method_line_id=self.destination_payment_method_line_id.id,
        ))._create_payments()
