# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

@openupgrade.migrate(use_env=True)
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_act_report_xml
        SET report_type = 'qweb-pdf', xslt_transform = true
        WHERE report_type = 'xslt'
        """,
    )
