# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

@openupgrade.migrate(use_env=True)
def migrate(env, version):
    env.cr.execute("SELECT name "
               "FROM ir_model_fields "
               "WHERE model='res.company' "
               "AND name='edespatch_usage'")
    if env.cr.fetchall():
        openupgrade.logged_query(env.cr,
            """
            UPDATE res_company 
            SET l10n_tr_edespatch_enabled = true
            WHERE einvoice_usage = 'edespatch'
            """,
        )
        openupgrade.logged_query(env.cr,
            """
            UPDATE res_partner 
            SET l10n_tr_is_driver = true
            WHERE type = 'driver'
            """,
        )
        if openupgrade.table_exists(
                env.cr, 'res_partner_stock_picking_rel'):
            openupgrade.logged_query(env.cr,
                 """
                 UPDATE stock_picking sp
                 SET l10n_tr_driver_id = rs.res_partner_id
                 FROM res_partner_stock_picking_rel rs
                 WHERE rs.stock_picking_id = sp.id
                 """,
             )
