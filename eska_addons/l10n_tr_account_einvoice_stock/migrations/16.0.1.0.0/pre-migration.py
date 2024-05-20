# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

xmlid_deletes = [
    "l10n_tr_account_einvoice_stock.view_picking_form_einvoice_stock",
    "l10n_tr_account_einvoice_stock.view_picking_form_einvoice",
]

@openupgrade.migrate(use_env=True)
def migrate(env, version):
    openupgrade.delete_records_safely_by_xml_id(env, xmlid_deletes, True)
