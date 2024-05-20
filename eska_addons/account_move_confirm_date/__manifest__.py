# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Invoice Confirm Date',
    'summary': 'Saves invoice confirmation date and time',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'views/account_move_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
