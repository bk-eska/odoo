# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale Order From Remaining',
    'summary': 'Create orders from sale remaining quantities',
    'version': '16.0.1.0.0',
    'category': 'Purchase',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale_stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_order_from_remaining_qty.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
}
