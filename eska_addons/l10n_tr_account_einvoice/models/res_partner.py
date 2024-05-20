# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_tr_einvoice_user = fields.Boolean(
        string="E-Invoice Registered User",
        compute='_compute_l10n_tr_einvoice_user',
        store=True,
    )

    l10n_tr_einvoice_sender_ids = fields.One2many(
        comodel_name='l10n_tr.einvoice.sender',
        inverse_name='partner_id',
        string='Senders',
        help='Senders of this partner.',
    )

    l10n_tr_einvoice_postbox_ids = fields.One2many(
        comodel_name='l10n_tr.einvoice.postbox',
        inverse_name='partner_id',
        string='Postboxes',
        help='Postboxes of this partner.',
    )

    l10n_tr_einvoice_import_invoice_lines = fields.Boolean(
        string='Import Incoming Invoice Lines',
    )

    l10n_tr_default_einvoice_profile = fields.Selection(
        selection=[
            ('TEMELFATURA', 'Temel Fatura'),
            ('TICARIFATURA', 'Ticari Fatura'),
            ('OZELFATURA', 'Özel Fatura'),
            ('KAMU', 'Kamu'),
            ('HKS', 'Hal Tipi'),
            ('ENERJI', 'Enerji'),
        ],
        string='Default Profile',
    )

    l10n_tr_default_einvoice_postbox = fields.Many2one(
        comodel_name='l10n_tr.einvoice.postbox',
        string='Default Postbox',
        domain="[('partner_id', '=', id)]",
        help='Default e-invoice postbox of this partner.',
    )

    @api.depends('vat', 'country_id')
    def _compute_l10n_tr_einvoice_user(self):
        users_obj = self.env['l10n_tr.einvoice.user']
        pb_obj = self.env['l10n_tr.einvoice.postbox']
        for rec in self:
            postboxes = []
            is_einvoice = False
            if not rec.parent_id:
                if rec.vat and (rec.vat[:2] == 'TR' or
                                rec.country_id.code == 'TR'):
                    vat = rec.ubltr_get_vat()
                    if vat and vat not in [
                        '1234567890',
                        '11111111111',
                        '2222222222',
                    ]:
                        postboxes = users_obj.search(
                            [('identifier', '=', rec.ubltr_get_vat()),
                        ])
                        if len(postboxes) > 0:
                            is_einvoice = True
            if not is_einvoice and not rec.l10n_tr_einvoice_user:
                continue
            if not is_einvoice and rec.l10n_tr_einvoice_user:
                # left einvoice user
                rec.l10n_tr_einvoice_user = False
            elif is_einvoice and not rec.l10n_tr_einvoice_user:
                # new einvoice user
                rec.l10n_tr_einvoice_user = True
            # first disable deleted postboxes
            for pb in rec.l10n_tr_einvoice_postbox_ids:
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
                        pb_obj.sudo().create({
                            'name': postbox.alias,
                            'partner_id': rec.id,
                        })
