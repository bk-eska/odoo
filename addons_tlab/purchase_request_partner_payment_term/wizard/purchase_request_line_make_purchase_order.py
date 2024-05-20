# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order"

    def _prepare_purchase_order(self, picking_type, group_id, company, origin):
        res = super()._prepare_purchase_order(picking_type, group_id, company, origin)
        if self.supplier_id.property_supplier_payment_term_id:
            res['payment_term_id'] = self.supplier_id.property_supplier_payment_term_id.id
        return res
