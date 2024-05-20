# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'barcodes.barcode_events_mixin']

    def on_barcode_scanned(self, barcode):
        self.ensure_one()
        if self.state in ['done', 'cancel']:
            return
        product = self.env['product.product'].search([
            '|', ('barcode', '=', barcode),
            ('default_code', '=', barcode),
        ], limit=1)
        if product:
            order_lines = self.order_line.filtered(
                lambda r: r.product_id == product)
            if order_lines:
                order_line = order_lines[0]
                order_line.product_uom_qty += 1
            else:
                newId = self.order_line.new({
                    'product_id': product.id,
                    'product_uom_qty': 1.0,
                })
                self.order_line += newId
        else:
            raise UserError(
                _('Cannot find a product for %s!') % barcode)
