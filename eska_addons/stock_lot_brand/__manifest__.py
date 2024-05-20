# Copyright 2024 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Stock Lot Brand',
    'summary': 'Manage brands on lot/serial.',
    'version': '16.0.1.0.0',
    'category': 'Stock',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'product_brand',
    ],
    'data': [
        'views/product_template_views.xml',
        'views/production_lot_views.xml',
        'views/stock_move_views.xml',
        'views/stock_quant_views.xml',
    ],
    'installable': True,
}
