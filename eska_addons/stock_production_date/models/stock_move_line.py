# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    production_date = fields.Datetime(
        string='Production Date',
        help='This is the date on which the goods with this serial number were produced.',
    )


    def _get_value_production_lot(self):
        res = super()._get_value_production_lot()
        if self.production_date:
            res.update({
                'production_date': self.production_date,
            })
        return res
