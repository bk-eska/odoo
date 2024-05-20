# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class L10nTrEinvoicePostbox(models.Model):

    _name = 'l10n_tr.einvoice.postbox'
    _description = 'E-Invoice Postboxes'

    active = fields.Boolean(
        string="Active",
        default=True,
    )

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

    journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Journal',
    )

    date_last_check = fields.Datetime(
        string="Last Check Date",
        default=fields.Datetime.now,
    )

    def get_invoices(self):
        for postbox in self:
            if postbox.company_id.vat:
                result = postbox.company_id.einvoice_get_envelopes(
                    postbox.name, 'INVOICE', postbox.date_last_check)
                postbox.date_last_check = result

    def update_invoices(self):
        for postbox in self:
            invoices = self.env['account.move'].search([
                ('l10n_tr_einvoice_state', '=', 'sent'),
                ('l10n_tr_einvoice_postbox_id', '=', postbox.id),
                ('move_type', 'in', ['in_invoice', 'in_refund']),
            ])
            if invoices:
                invoices.einvoice_get_status()
