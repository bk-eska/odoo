# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountTransferModel(models.Model):
    _inherit = "account.transfer.model"

    l10n_tr_use_reflection_account = fields.Boolean(
        string='Use Reflection Account',
        help='Reflection accounts of the account will be used if selected',
    )

    def _get_non_filtered_auto_transfer_move_line_values(
            self, lines, start_date, end_date):
        res = super()._get_non_filtered_auto_transfer_move_line_values(
            lines, start_date, end_date)
        if self.l10n_tr_use_reflection_account:
            for line in res:
                account = self.env['account.account'].browse(line['account_id'])
                if account.l10n_tr_reflection_account_id:
                    line['account_id'] = account.l10n_tr_reflection_account_id.id
        return res