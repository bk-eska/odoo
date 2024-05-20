# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def _post(self, soft=True):
        for rec in self:
            if (
                    rec.move_type != 'entry'
                    and rec.fiscal_position_id.vat_required
                    and not rec.commercial_partner_id.vat
            ):
                raise UserError(_('Partner tax number is missing!'))
        return super(AccountMove, self)._post(soft)
