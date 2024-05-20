# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Purchase Order Lot Selection',
    'summary': 'Purchase Order Lot Selection',
    'version': '16.0.1.0.0',
    'category': 'Purchase',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'purchase_stock',
        'stock_restrict_lot',
    ],
    'data': [
        'view/purchase_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
