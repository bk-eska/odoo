# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

@openupgrade.migrate(use_env=True)
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_journal
        SET l10n_tr_cash_payment_type = l10n_tr_payment_type
        WHERE type = 'cash'
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_journal
        SET l10n_tr_bank_payment_type = l10n_tr_payment_type
        WHERE type = 'bank'
        """,
    )
    env['account.journal'].search([
        ('type', '=', 'sale'),
        ('company_id.country_id.code', '=', 'TR')
    ]).write({'invoice_reference_model': 'tr'})