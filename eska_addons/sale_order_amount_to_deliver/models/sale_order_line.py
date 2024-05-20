# Copyright 2024 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _convert_to_tax_base_line_dict(self):
        self.ensure_one()
        if self.env.context.get('amount_to_deliver'):
            return self.env['account.tax']._convert_to_tax_base_line_dict(
                self,
                partner=self.order_id.partner_id,
                currency=self.order_id.currency_id,
                product=self.product_id,
                taxes=self.tax_id,
                price_unit=self.price_unit,
                quantity=self.qty_to_deliver,
                discount=self.discount,
                price_subtotal=self.price_subtotal,
            )
        else:
            return super(SaleOrderLine, self)._convert_to_tax_base_line_dict()
