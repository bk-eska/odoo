# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class L10nTrEdespatchSender(models.Model):

    _name = 'l10n_tr.edespatch.sender'
    _description = 'E-Despatch Senders'

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

    def get_receipts(self):
        for sender in self:
            result = sender.company_id.edespatch_get_envelopes(
                sender.name, 'ENVELOPE', sender.date_last_check)
            sender.date_last_check = result

    def update_despatches(self):
        for sender in self:
            pickings = self.env['stock.picking'].search([
                ('l10n_tr_edespatch_state', '=', 'sent'),
                ('l10n_tr_edespatch_sender_id', '=', sender.id),
                ('picking_type_code', '=', 'outgoing'),
            ])
            if pickings:
                pickings.edespatch_get_status()
