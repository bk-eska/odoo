# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

@openupgrade.migrate(use_env=True)
def migrate(env, version):
    if not openupgrade.table_exists(
            env.cr, 'account_account_account_transfer_mapping_rel'):
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE account_account aa 
            SET l10n_tr_reflection_account_id = atm.transfer_account_id
            FROM account_transfer_mapping atm
            INNER JOIN account_account_account_transfer_mapping_rel amr
            ON atm.id = amr.account_transfer_mapping_id
            WHERE amr.account_account_id = aa.id
            """,
        )
