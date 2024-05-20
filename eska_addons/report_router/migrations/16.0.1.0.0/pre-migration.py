# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

field_renames = [
    ('ir.actions.reports.route', 'ir_actions_report_route', 'router_id', 'parent_id'),
]

def rename_fields(env, field):
    cr = env.cr
    cr.execute('SELECT name FROM ir_model_fields WHERE model=%s AND name=%s',
        (field[0], field[3]))
    if cr.fetchall():
        return
    cr.execute('SELECT name FROM ir_model_fields WHERE model=%s AND name=%s',
               (field[0], field[2]))
    if cr.fetchall():
        openupgrade.rename_fields(env, [field])

@openupgrade.migrate(use_env=True)
def migrate(env, version):
    for field in field_renames:
        rename_fields(env, field)
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_actions_report_route rr
        SET parent_id = dr.id
        FROM ir_act_report_xml dr
        inner JOIN ir_act_report_xml sr
        ON dr.report_name = sr.report_name
        WHERE dr.report_type <> 'router'
        AND sr.report_type = 'router'
        and rr.parent_id = sr.id
        """,
    )
