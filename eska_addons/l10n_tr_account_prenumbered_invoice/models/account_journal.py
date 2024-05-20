# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    l10n_tr_document_number_sequence = fields.Many2one(
        comodel_name='ir.sequence',
        string='Printed Invoice Number Sequence',
        help='This is used to number printed invoices',
    )

    l10n_tr_document_auto_number = fields.Boolean(
        string='Auto Number',
        help='Gives auto number on validate'
    )
