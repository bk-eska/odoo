# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale Unit Price Readonly',
    'summary': 'Sale unit price readonly',
    'version': '16.0.1.0.0',
    'category': 'Sale',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale_management',
    ],
    'data': [
        'security/security.xml',
        'views/sale_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}