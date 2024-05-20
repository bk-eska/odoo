# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class L10nTrEinvoiceSender(models.Model):

    _name = 'l10n_tr.einvoice.sender'
    _description = 'E-Invoice Senders'

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
    )

    name = fields.Char(
        string='Label',
        required=True,
    )

    date_last_check = fields.Datetime(
        string="Last Check Date",
        default=fields.Datetime.now,
    )

    def get_responses(self):
        for sender in self:
            result = sender.company_id.einvoice_get_envelopes(
                sender.name, 'APP_RESP', sender.date_last_check)
            sender.date_last_check = result

    def update_invoices(self):
        for sender in self:
            invoices = self.env['account.move'].search([
                ('l10n_tr_einvoice_state', '=', 'sent'),
                ('l10n_tr_einvoice_sender_id', '=', sender.id),
                ('move_type', 'in', ['out_invoice', 'out_refund']),
            ])
            if invoices:
                invoices.einvoice_get_status()
