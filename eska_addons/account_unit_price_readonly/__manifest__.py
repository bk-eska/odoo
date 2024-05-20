# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Unit Price Readonly',
    'summary': 'Account unit price readonly',
    'version': '16.0.1.0.0',
    'category': 'Account',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'security/security.xml',
        'views/account_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}