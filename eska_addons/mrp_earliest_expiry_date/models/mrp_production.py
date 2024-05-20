# Copyright 2021 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import datetime

from dateutil.relativedelta import relativedelta
from datetime import date
from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    earliest_expiry_date = fields.Date(
        string="Earliest Expire Date",
        compute='_compute_earliest_expiry_date',
    )

    def _compute_earliest_expiry_date(self):
        for record in self:
            lots = record.move_raw_ids.mapped('move_line_ids.lot_id').filtered(lambda ml: ml.expiration_date)
            expiries = lots.mapped('expiration_date')
            record.earliest_expiry_date = min(expiries) if expiries else False

    def _prepare_stock_lot_values(self):
        res = super()._prepare_stock_lot_values()
        if 'expiration_date' in res and self.earliest_expiry_date and res['expiration_date'] > self.earliest_expiry_date:
            res['expiration_date'] = self.earliest_expiry_date
        return res

