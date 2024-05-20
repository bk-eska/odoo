# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_tr_edespatch_user = fields.Boolean(
        string="E-Despatch Registered User",
        compute='_compute_l10n_tr_edespatch_user',
        store=True,
    )

    l10n_tr_edespatch_sender_ids = fields.One2many(
        comodel_name='l10n_tr.edespatch.sender',
        inverse_name='partner_id',
        string='E-Despatch Senders',
        help='E-Despatch Senders of this partner.',
    )

    l10n_tr_edespatch_postbox_ids = fields.One2many(
        comodel_name='l10n_tr.edespatch.postbox',
        inverse_name='partner_id',
        string='E-Despatch Postboxes',
        help='E-Despatch Postboxes of this partner.',
    )

    l10n_tr_default_edespatch_postbox = fields.Many2one(
        comodel_name='l10n_tr.edespatch.postbox',
        string='Default E-Despatch Postbox',
        domain="[('partner_id', '=', id)]",
        help='Default e-invoice postbox of this partner.',
    )

    @api.depends('vat', 'country_id')
    def _compute_l10n_tr_edespatch_user(self):
        users_obj = self.env['l10n_tr.edespatch.user']
        pb_obj = self.env['l10n_tr.edespatch.postbox']
        for rec in self:
            postboxes = []
            is_edespatch = False
            if not rec.parent_id:
                if rec.vat and (rec.vat[:2] == 'TR' or
                                rec.country_id.code == 'TR'):
                    postboxes = users_obj.search(
                        [('identifier', '=', rec.ubltr_get_vat()),
                    ])
                    if len(postboxes)>0:
                        is_edespatch = True

            if not is_edespatch and not rec.l10n_tr_edespatch_user:
                continue
            if not is_edespatch and rec.l10n_tr_edespatch_user:
                # left edespatch user
                rec.l10n_tr_edespatch_user = False
            elif is_edespatch and not rec.l10n_tr_edespatch_user:
                # new edespatch user
                rec.l10n_tr_edespatch_user = True
            # first disable deleted postboxes
            for pb in rec.l10n_tr_edespatch_postbox_ids:
                found = False
                if rec.vat:
                    found = users_obj.search([
                        ('alias', '=', pb.name),
                        ('identifier', '=', rec.ubltr_get_vat()),
                    ], limit=1)
                if not found:
                    pb.active = False
            # create or enable new postboxes
            for postbox in postboxes:
                found = pb_obj.search([
                    ('name', '=', postbox.alias),
                    ('partner_id', '=', rec.id),
                    ('active', '=', False),
                ], limit=1)
                if found:
                    # reactivate
                    found.active = True
                else:
                    found = pb_obj.search([
                        ('name', '=', postbox.alias),
                        ('partner_id', '=', rec.id),
                    ], limit=1)
                    if not found:
                        # create
                        pb_obj.create({
                            'name': postbox.alias,
                            'partner_id': rec.id,
                        })

