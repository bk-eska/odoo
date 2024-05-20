# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

xmlid_renames = [
    (
        "currency_inverse_rate.decimal_currency_inverse_rate",
        "currency_rate_precision.decimal_currency_inverse_rate",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, xmlid_renames)
