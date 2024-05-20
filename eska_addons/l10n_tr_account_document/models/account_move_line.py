# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _compute_name(self):
        result = super()._compute_name()
        for line in self.filtered(lambda l: l.display_type == 'payment_term' and
                                            l.move_id.l10n_tr_use_document and
                                            l.move_id.l10n_tr_document_number):
            line.name = line.move_id.l10n_tr_document_number
        return result
