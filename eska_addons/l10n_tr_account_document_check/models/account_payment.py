# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.onchange("l10n_latam_check_number", "l10n_latam_check_id")
    def onchange_check_fields(self):
        self.l10n_tr_document_number = \
            self.l10n_latam_check_id.l10n_latam_check_number \
                if self.l10n_latam_check_id else self.l10n_latam_check_number

    @api.model_create_multi
    def create(self, vals_list):
        moves = super(AccountPayment, self).create(vals_list)
        for move in moves:
            if not move.l10n_tr_document_number and move.l10n_latam_check_id:
                move.l10n_tr_document_number = \
                    move.l10n_latam_check_id.l10n_latam_check_number
        return moves

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        res = super()._prepare_move_line_default_vals(
            write_off_line_vals=write_off_line_vals)
        date_maturity = False
        if self.l10n_latam_check_id and \
                self.l10n_latam_check_id.l10n_latam_check_payment_date:
            date_maturity = \
                self.l10n_latam_check_id.l10n_latam_check_payment_date
        elif self.l10n_latam_check_payment_date:
            date_maturity = self.l10n_latam_check_payment_date
        if date_maturity:
            res[0].update({'date_maturity': date_maturity})
        return res

    def _synchronize_to_moves(self, changed_fields):
        if 'l10n_latam_check_payment_date' in changed_fields:
            changed_fields.add('amount')
        return super(AccountPayment, self)._synchronize_to_moves(
            changed_fields)