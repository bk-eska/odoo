# Copyright 2021 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order"

    def _prepare_purchase_order_line(self, po, item):
        values = super(PurchaseRequestLineMakePurchaseOrder,
                       self)._prepare_purchase_order_line(po, item)
        values['name'] = item.name
        return values
