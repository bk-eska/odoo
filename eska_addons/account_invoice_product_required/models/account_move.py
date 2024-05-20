# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def _post(self, soft=True):
        for rec in self.filtered(lambda l: l.move_type != 'entry'):
            for line in rec.invoice_line_ids:
                if not line.product_id and not line.display_type:
                    raise UserError(_('Please select product on all invoice lines!'))
        return super(AccountMove, self)._post(soft)
