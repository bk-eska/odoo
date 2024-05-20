# Copyright 2019 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, Command


class ResUsers(models.Model):
    _inherit = "res.users"

    journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Journal',
        copy=False,
    )

    def action_create_journal(self):
        Journal = self.env['account.journal']
        for rec in self:
            journal = Journal.create({
                'name': rec.name,
                'code': Journal.get_next_bank_cash_default_code('cash', self.env.company),
                'type': 'cash',
                'company_id': self.env.company.id,
                'use_in_collections': True,
                'user_id': rec.id,
                'outbound_payment_method_line_ids': [
                    Command.create({'payment_method_id': self.env.ref(
                        'account.account_payment_method_manual_out').id}),
                    Command.create({'payment_method_id': self.env.ref(
                        'l10n_latam_check.account_payment_method_out_third_party_checks').id}),
                ],
                'inbound_payment_method_line_ids': [
                    Command.create({'payment_method_id': self.env.ref(
                        'account.account_payment_method_manual_in').id}),
                    Command.create({'payment_method_id': self.env.ref(
                        'l10n_latam_check.account_payment_method_new_third_party_checks').id}),
                    Command.create({'payment_method_id': self.env.ref(
                        'l10n_latam_check.account_payment_method_in_third_party_checks').id}),
                ]
            })
            method_line_ids = journal.outbound_payment_method_line_ids | journal.inbound_payment_method_line_ids
            for method_line in method_line_ids:
                method_line.payment_account_id = journal.default_account_id
            rec.journal_id = journal.id

