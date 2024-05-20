# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class DateRangeRenumber(models.TransientModel):
    _name = "date.range.renumber"
    _description = "Date Range Renumber"

    l10n_tr_next_move_sequence = fields.Integer(
        string='Move Sequence Number Start',
        required=True,
        default=0,
        help='Move sequences will start counting on this number',
    )

    l10n_tr_next_line_sequence = fields.Integer(
        string='Line Sequence Number Start',
        required=True,
        default=0,
        help='Line sequences will start counting on this number',
    )

    l10n_tr_ignore_zero_amount = fields.Boolean(
        string='Ignore Zero Amount Entries',
        default=True,
        help='Entries with no amount will not be renumbered',
    )

    def renumber(self):
        next_move_sequence = self.l10n_tr_next_move_sequence
        next_line_sequence = self.l10n_tr_next_line_sequence
        move_obj = self.env['account.move']
        date_range_ids = self.env['date.range'].browse(self.env.context.get('active_ids', []))
        for range in date_range_ids.sorted(key='date_start'):
            move_sequence_number_start = next_move_sequence - 1
            line_sequence_number_start = next_line_sequence - 1
            move_ids = move_obj.search([
                ('date', '>=', range.date_start),
                ('date', '<=', range.date_end),
                ('journal_id.l10n_tr_renumber', '=', True),
                ('state', '=', 'posted'),
                ('company_id', '=', range.company_id.id),
            ], order='date,id')
            if move_ids:
                for move in move_ids:
                    line_ids = move.line_ids
                    if self.l10n_tr_ignore_zero_amount:
                        line_ids = line_ids.filtered(lambda l: l.debit > 0 or l.credit > 0)
                    if not line_ids:
                        continue
                    self.env.cr.execute('UPDATE account_move SET l10n_tr_move_sequence_number=%s WHERE id=%s', (next_move_sequence, move.id))
                    next_move_sequence += 1
                    for line in line_ids:
                        self.env.cr.execute('UPDATE account_move_line SET l10n_tr_line_sequence_number=%s WHERE id=%s',(next_move_sequence, line.id))
                        next_line_sequence += 1
                if next_move_sequence > move_sequence_number_start + 1:
                    move_sequence_number_start += 1
                    line_sequence_number_start += 1
                range.write({
                    'l10n_tr_move_sequence_number_start': move_sequence_number_start,
                    'l10n_tr_move_sequence_number_stop': next_move_sequence - 1,
                    'l10n_tr_line_sequence_number_start': line_sequence_number_start,
                    'l10n_tr_line_sequence_number_stop': next_line_sequence - 1,
                })
