# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale Order Relocate Warehouse Fields',
    'summary': 'Relocates the warehouse informations on the sale form.',
    'version': '16.0.1.0.0',
    'category': 'Sales/Sales',
    'license': 'AGPL-3',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'depends': [
        'sale_stock',
    ],
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
}
