# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Yavuzpres Default Company',
    'summary': 'Set the current company as default on partner',
    'version': '16.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'views/res_users_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
