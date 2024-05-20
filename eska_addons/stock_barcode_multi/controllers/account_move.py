# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http, _
from odoo.addons.stock_barcode.controllers.stock_barcode import StockBarcodeController

class StockBarcodeControllerMulti(StockBarcodeController):

    @http.route('/stock_barcode/get_specific_barcode_data', type='json', auth='user')
    def get_specific_barcode_data(self, barcode, model_name, domains_by_model=False):
        result = super().get_specific_barcode_data(barcode, model_name, domains_by_model)
        if 'product.product' in result:
            for product in result['product.product']:
                product['barcode'] = barcode
        return result
