# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    def _update_discount_display_fields(self):
        for line in self:
            line.price_total_no_discount = 0
            line.discount_total = 0
            price = line.product_id.lst_price
            taxes = line.tax_id.compute_all(
                price,
                line.order_id.currency_id,
                line.product_uom_qty,
                product=line.product_id,
                partner=line.order_id.partner_shipping_id,
            )

            price_total_no_discount = taxes["total_included"]
            discount_total = price_total_no_discount - line.price_total

            line.update(
                {
                    "discount_total": discount_total,
                    "price_total_no_discount": price_total_no_discount,
                }
            )

