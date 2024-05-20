# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Expense Groups',
    'summary': 'Define account groups for expenses and specify it on analytic and products',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'auto_install': False,
    'depends': [
         'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/account_expense_group_security.xml',
        'views/account_analytic_account_view.xml',
        'views/account_expense_group_view.xml',
        'views/product_template_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}

