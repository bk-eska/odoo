# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResBank(models.Model):
    _inherit = 'res.bank'

    l10n_tr_eft_code = fields.Char(
        string="EFT Code",
        help="EFT Code used in Turkey",
    )
