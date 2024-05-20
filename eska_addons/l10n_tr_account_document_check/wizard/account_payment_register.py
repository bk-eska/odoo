# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    @api.onchange("check_number")
    def onchange_check_number(self):
        self.document_number = self.check_number

