# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale Order Lines Product Image',
    'summary': 'Adds an Image of the Product to Sale Order Lines',
    'version': '16.0.1.0.0',
    'category': 'Sale',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale_stock',
    ],
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
}
