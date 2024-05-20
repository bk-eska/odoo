
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_rfq_qty = fields.Float(
        string='Product RFQ Qty',
        compute='_compute_product_rfq_count',
    )

    rfq_count = fields.Integer(
        string='RFQ Count',
        compute='_compute_product_rfq_count',
    )

    def _compute_product_rfq_count(self):
        for product in self:
            rfq_ids = self.env['purchase.order.line'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'draft'),
            ])
            product.product_rfq_qty = sum(rfq_ids.mapped('product_qty'))
            product.rfq_count = len(rfq_ids.mapped('order_id'))


