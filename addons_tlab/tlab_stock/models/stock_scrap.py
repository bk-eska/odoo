# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    uts_description = fields.Char(
        string='UTS Description',
        size=50,
    )
