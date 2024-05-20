# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockLot(models.Model):
    _inherit = 'stock.lot'

    production_date = fields.Datetime(
        string='Production Date',
        help='This is the date on which the goods with this serial number were produced.',
    )