# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Expense Groups',
    'summary': 'Türkiye Gider Grupları',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account_expense_group',
    ],
    'data': [
        'data/account_expense_group.xml',
    ],
    'installable': True,
    'auto_install': True,
}
