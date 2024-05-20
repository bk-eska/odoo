# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Stock Reporting Currency',
    'summary': 'Stock reporting currency',
    'version': '16.0.1.0.0',
    'category': 'Stock',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'stock_account',
        'base_reporting_currency',
    ],
    'data': [
        'views/product_template_view.xml',
        'views/product_product_view.xml',
        'views/stock_quant_view.xml',
        'views/stock_valuation_layer_view.xml',
    ],
    'installable': True,
}
