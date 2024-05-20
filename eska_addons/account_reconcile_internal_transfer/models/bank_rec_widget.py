from odoo import fields, models

class BankRecWidget(models.Model):
    _inherit = 'bank.rec.widget'

    form_account_id = fields.Many2one(
        domain="[('account_type', '!=', 'off_balance'), "
               "('company_id', '=', company_id), "
               "('deprecated', '=', False)]",
    )
