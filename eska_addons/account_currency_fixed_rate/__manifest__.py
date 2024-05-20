# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Currency Fixed Rate',
    'summary': 'Use fixed currency rates on documents',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account_currency_rate',
        'currency_fixed_rate',
    ],
    'data': [
        'wizard/account_convert_currency_view.xml',
        'wizard/account_payment_register_view.xml',
        'views/account_move_view.xml',
        'views/account_payment_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
