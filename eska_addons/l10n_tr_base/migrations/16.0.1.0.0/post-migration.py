# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

@openupgrade.migrate(use_env=True)
def migrate(env, version):
    cr = env.cr
    env.cr.execute("SELECT name FROM ir_model_fields "
               "WHERE model='account.fiscal.position.category' AND name='code'")
    if env.cr.fetchall():
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE account_fiscal_position f
            SET l10n_tr_fp_type = c.code
            FROM account_fiscal_position_category c
            WHERE f.category_id = c.id
            """,
        )
