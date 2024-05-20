# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    invoice_reference_model = fields.Selection(selection_add=[
        ('tr', 'Turkey')
    ], ondelete={'tr': lambda recs: recs.write({'invoice_reference_model': 'odoo'})})

    l10n_tr_use_document = fields.Boolean(
        related='company_id.l10n_tr_use_document',
    )

    l10n_tr_payment_type = fields.Selection(
        selection=[
            ('cash', 'Cash'),
            ('bank', 'Bank'),
            ('credit_card', 'Credit Card'),
            ('check', 'Check'),
            ('promissory', 'Promissory Note'),
        ],
        string='Payment Type',
        compute='_compute_l10n_tr_payment_type',
        store=True,
    )

    l10n_tr_cash_payment_type = fields.Selection(
        selection=[
            ('cash', 'Cash'),
            ('check', 'Check'),
            ('promissory', 'Promissory Note'),
        ],
        string='Cash Payment Type',
        default='cash',
    )

    l10n_tr_bank_payment_type = fields.Selection(
        selection=[
            ('bank', 'Bank'),
            ('credit_card', 'Credit Card'),
            ('check', 'Check'),
            ('promissory', 'Promissory Note'),
        ],
        string='Bank Payment Type',
        default='bank',
    )

    @api.depends('type', 'l10n_tr_cash_payment_type', 'l10n_tr_bank_payment_type')
    def _compute_l10n_tr_payment_type(self):
        for journal in self:
            if journal.type == 'cash':
                journal.l10n_tr_payment_type = \
                        journal.l10n_tr_cash_payment_type or 'cash'
            elif journal.type == 'bank':
                journal.l10n_tr_payment_type = \
                        journal.l10n_tr_bank_payment_type or 'bank'
            else:
                journal.l10n_tr_payment_type = False
