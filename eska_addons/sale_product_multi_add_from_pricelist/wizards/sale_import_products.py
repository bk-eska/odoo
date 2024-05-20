from odoo import fields, models


class SaleImportProductsPricelist(models.TransientModel):
    _inherit = "sale.import.products"

    def _multi_add_price_list(self):
        pricelist_id = self.env['product.pricelist'].browse(self._context.get('pricelist_id'))
        product_ids = pricelist_id.item_ids.mapped('product_id')
        return [('id', 'in', product_ids.ids)] if pricelist_id else []

    products = fields.Many2many(
        domain=_multi_add_price_list,
    )
