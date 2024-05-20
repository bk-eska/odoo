# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

@openupgrade.migrate(use_env=True)
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        DELETE FROM ir_model_data
        WHERE module = 'l10n_tr_account_fiscal_year_closing'
        AND model = 'account.journal'
        """,
    )
