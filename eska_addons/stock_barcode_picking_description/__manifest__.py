# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Stock Barcode Picking Description",
    "version": "16.0.1.0.0",
    "summary": "Stock Barcode Picking Description",
    "author": 'Eska',
    "website": 'http://www.eskayazilim.com.tr',
    "license": 'AGPL-3',
    "category": "Stock",
    "depends": [
        'stock_barcode',
    ],
    'data': [
        "views/stock_move_line_views.xml",
    ],
    'installable': True,
    'auto_install': False,
}
