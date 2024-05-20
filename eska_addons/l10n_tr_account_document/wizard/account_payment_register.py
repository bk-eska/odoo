# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    l10n_tr_use_document = fields.Boolean(
        related='company_id.l10n_tr_use_document',
    )

    l10n_tr_document_number = fields.Char(
        string='Document Number',
    )

    def _create_payment_vals_from_wizard(self, batch_result):
        res = super(AccountPaymentRegister,
                    self)._create_payment_vals_from_wizard(batch_result)
        res['l10n_tr_document_number'] = self.l10n_tr_document_number
        return res