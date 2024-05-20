# Copyright 2021 Eska Technology LLC (www.eskaweb.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _
from odoo.exceptions import UserError


class CollectionOrderLine(models.Model):
    _name = 'collection.order.line'
    _description = 'Collection Order Line'

    def _compute_collected_amount(self):
        for line in self:
            line.collected_amount = sum(
                line.payment_ids.filtered(
                    lambda x: x.state != 'cancel' and x.amount_company_currency_signed > 0.0).mapped('amount'))

    name = fields.Text(
        string='Description',
    )

    sequence = fields.Integer(
        default=10,
        help="Gives the sequence of this line when displaying the orders."
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        required=True,
        readonly=True,
        states={'new': [('readonly', False)]},
    )

    partner_address = fields.Char(
        related='partner_id.contact_address',
        string='Address'
    )

    collection_order_id = fields.Many2one(
        comodel_name='collection.order',
        string='Collection Order',
        ondelete='cascade',
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        related='collection_order_id.company_id',
    )

    state = fields.Selection(
        string='State',
        related='collection_order_id.state',
    )

    receivable_amount = fields.Monetary(
        string='Receivable Amount',
        currency_field='currency_id',
        related='partner_id.credit',
    )

    collected_amount = fields.Monetary(
        compute='_compute_collected_amount',
        string='Collected Amount',
        currency_field='currency_id',
    )

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        related='collection_order_id.currency_id',
    )

    payment_ids = fields.One2many(
        comodel_name='account.payment',
        inverse_name='collection_line_id',
        string='Payments',
        readonly=True
    )

    def unlink(self):
        for line in self:
            if line.collected_amount != 0 or line.payment_ids.filtered(lambda l: l.state != 'cancel'):
                raise UserError(_('You cannot delete a line which has collected amount!'))
        return super(CollectionOrderLine, self).unlink()

    def action_register_payment(self):
        return {
            'name': _('Register Payment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'account.payment',
            'context': dict(
                self.env.context,
                default_journal_id=self.collection_order_id.journal_id.id,
                default_payment_type='inbound',
                default_partner_id=self.partner_id.id,
                default_collection_line_id=self.id,
                default_amount=self.receivable_amount,
            ),
        }

