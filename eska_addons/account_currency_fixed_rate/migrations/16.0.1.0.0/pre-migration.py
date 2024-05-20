# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

module_renames = [
    ('account_currency_inverse_fixed_rate', 'account_currency_fixed_rate'),
]

def rename_modules(env, module):
    if env["ir.module.module"].search(
            [("name", "=", module[0])]):
        openupgrade.update_module_names(
            env.cr, [(module[0], module[1])], merge_modules=True)

@openupgrade.migrate(use_env=True)
def migrate(env, version):
    for module in module_renames:
        rename_modules(env, module)
