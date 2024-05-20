# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    l10n_tr_renumber = fields.Boolean(
        string='Renumber',
        default=True,
        help='If checked, moves and move lines of this journal will be renumbered.'
    )
