# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Route Sale',
    'summary': 'Add route to sale',
    'version': '16.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'base_route',
    ],
    'data': [
        "views/sale_order_view.xml",
    ],
    'installable': True,
    'auto_install': False,
}
