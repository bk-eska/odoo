from odoo import api, models

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.depends('journal_id', 'partner_id', 'partner_type', 'is_internal_transfer', 'destination_journal_id')
    def _compute_destination_account_id(self):
        result = super()._compute_destination_account_id()
        for pay in self.filtered(lambda p: p.is_internal_transfer and p.journal_id.transfer_account_id):
            pay.destination_account_id = pay.journal_id.transfer_account_id
