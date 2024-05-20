# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Purchase Order Barcode',
    'summary': 'Use barcode scanner in purchase order.',
    'version': '16.0.1.0.0',
    'category': 'Purchase',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'auto_install': False,
    'depends': [
        'barcodes',
        'purchase',
    ],
    'data': [
        'views/purchase_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}