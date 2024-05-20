# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _reverse_moves(self, default_values_list=None, cancel=False):
        res = super(AccountMove, self)._reverse_moves(default_values_list, cancel)
        for move in res.filtered(lambda m: m.move_type in
                                           ['out_refund', 'in_refund']):
            for line in move.line_ids.filtered(
                    lambda l: l.product_id and l.display_type == 'product'):
                accounts = line.product_id.product_tmpl_id.with_context(
                    move_type=move.move_type).get_product_accounts()
                if line.move_id.is_sale_document(include_receipts=True):
                    line.account_id = accounts['income'] or line.account_id
                elif line.move_id.is_purchase_document(include_receipts=True):
                    line.account_id = accounts['expense'] or line.account_id
        return res