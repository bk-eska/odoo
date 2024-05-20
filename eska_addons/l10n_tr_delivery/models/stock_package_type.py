# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PackageType(models.Model):
    _inherit = 'stock.package.type'

    l10n_tr_unece_code = fields.Char(
        string="UNECE Code",
        help="Standard nomenclature of the United Nations Economic "
             "Commission for Europe (UNECE).",
    )
