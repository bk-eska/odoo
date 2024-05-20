# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    l10n_tr_einvoice_enabled = fields.Boolean(
        string='E-Invoice Enabled',
        related='company_id.l10n_tr_einvoice_enabled'
    )

    l10n_tr_einvoice_sender_id = fields.Many2one(
        comodel_name='l10n_tr.einvoice.sender',
        string='E-Invoice Sender',
    )

    l10n_tr_einvoice_sequence = fields.Many2one(
        comodel_name='ir.sequence',
        string='E-Invoice Number Sequence',
    )

    l10n_tr_earchive_sequence = fields.Many2one(
        comodel_name='ir.sequence',
        string='E-Archive Number Sequence',
    )

    l10n_tr_einvoice_postbox_ids = fields.One2many(
        comodel_name='l10n_tr.einvoice.postbox',
        inverse_name='journal_id',
        string='Postboxes',
        help='Postboxes related with this journals.',
    )

    l10n_tr_branch_id = fields.Many2one(
        comodel_name='res.partner',
        string='Branch',
        help='Branch which will be used in e-documents.',
    )