# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    l10n_tr_line_sequence_number = fields.Integer(
        string='Line Sequence Number',
        readonly=True,
    )

    l10n_tr_move_sequence_number = fields.Integer(
        related='move_id.l10n_tr_move_sequence_number',
        string='Move Sequence Number',
        readonly=True,
    )
