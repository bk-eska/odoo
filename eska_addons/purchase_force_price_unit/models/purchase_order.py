# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        for order in self:
            for line in order.order_line.filtered(lambda x: not x.display_type):
                if line.price_unit == 0:
                    raise UserError(_(
                        'Please select price unit for %s aside from 0 on all order lines!' % line.product_id.name))
        return super(PurchaseOrder, self).button_confirm()
