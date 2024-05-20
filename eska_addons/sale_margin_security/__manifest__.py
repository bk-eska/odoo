# Copyright 2024 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale Margin Security',
    'summary': 'This module hides margin fields from non-admin users.',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale_margin',
    ],
    'data': [
        'security/security.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}