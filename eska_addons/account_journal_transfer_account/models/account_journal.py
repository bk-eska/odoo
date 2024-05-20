from odoo import fields, models

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    transfer_account_id = fields.Many2one(
        comodel_name='account.account',
        string="Internal Transfer Account",
        domain=[
            ('reconcile', '=', True),
            ('account_type', '=', 'asset_current'),
            ('deprecated', '=', False),
        ],
        help="Overrides the internal transfer account specified on the company",
    )