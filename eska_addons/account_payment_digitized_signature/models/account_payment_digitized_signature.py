from odoo import models, Command, fields, api, _


class AccountPaymentDigitizedSignature(models.Model):
    _inherit = "account.payment"

    signature = fields.Image(string='Signature', help='Signature', copy=False, attachment=True, tracking=True)

    def action_account_unsign(self):
        self.signature = False

    @api.depends('signature')
    def _compute_is_signed(self):
        for account in self:
            account.is_signed = account.signature