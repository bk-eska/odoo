# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, _
from odoo.exceptions import UserError


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def _apply_inventory(self):
        if not self.user_has_groups('tlab_stock.group_stock_adjustment'):
            raise UserError(_("You are not allowed to apply inventory adjustments."))
        return super(StockQuant, self)._apply_inventory()
