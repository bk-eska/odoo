# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class L10nTrEdespatchPostbox(models.Model):

    _name = 'l10n_tr.edespatch.postbox'
    _description = 'E-Despatch Postboxes'

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

    picking_type_id = fields.Many2one(
        comodel_name='stock.picking.type',
        string='Operation Type',
    )

    date_last_check = fields.Datetime(
        string="Last Check Date",
        default=fields.Datetime.now,
    )

    def get_despatches(self):
        for postbox in self:
            if postbox.company_id.vat:
                result = postbox.company_id.edespatch_get_envelopes(
                    postbox.name, 'ENVELOPE', postbox.date_last_check)
                postbox.date_last_check = result

    def update_despatches(self):
        for postbox in self:
            pickings = self.env['stock.picking'].search([
                ('l10n_tr_edespatch_state', '=', 'sent'),
                ('l10n_tr_edespatch_postbox_id', '=', postbox.id),
                ('picking_type_code', '=', 'incoming'),
            ])
            if pickings:
                pickings.edespatch_get_status()
