# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

@openupgrade.migrate(use_env=True)
def migrate(env, version):
    env.cr.execute("SELECT name "
               "FROM ir_model_fields "
               "WHERE model='res.company' "
               "AND name='einvoice_usage'")
    if env.cr.fetchall():
        openupgrade.logged_query(env.cr,
            """
            UPDATE res_company 
            SET l10n_tr_einvoice_enabled = true
            WHERE einvoice_usage IN ('einvoice', 'earchive')
            """,
        )
