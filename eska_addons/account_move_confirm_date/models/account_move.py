# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    confirm_date = fields.Datetime(
        string='Confirm Date',
        readonly=True,
        copy=False,
    )

    def _post(self, soft=True):
        res = super(AccountMove, self)._post(soft)
        self.write({'confirm_date': fields.Datetime.now()})
        return res

    def button_draft(self):
        res = super(AccountMove, self).button_draft()
        self.write({'confirm_date': False})
        return res


