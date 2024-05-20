# Copyright 2024 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _action_done(self):
        for rec in self:
            if rec.picking_type_code in ['outgoing', 'internal']:
                if any(m.product_uom_qty < m.quantity_done for m in rec.move_ids_without_package):
                    raise UserError(_('You cannot transfer more quantity than demanded!'))
        return super(StockPicking, self)._action_done()
