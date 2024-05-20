# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class DateRange(models.Model):
    _inherit = "date.range"

    l10n_tr_move_sequence_number_start = fields.Integer(
        string='Move Sequence Number Start',
        readonly=True,
        default=0,
    )

    l10n_tr_move_sequence_number_stop = fields.Integer(
        string='Move Sequence Number Stop',
        readonly=True,
        default=0,
    )

    l10n_tr_line_sequence_number_start = fields.Integer(
        string='Line Sequence Number Start',
        readonly=True,
        default=0,
    )

    l10n_tr_line_sequence_number_stop = fields.Integer(
        string='Line Sequence Number Stop',
        readonly=True,
        default=0,
    )
