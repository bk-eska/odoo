# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Analytic Account Reporting Currency',
    'summary': 'Analytic Account Reporting Currency',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'auto_install': False,
    'depends': [
        'analytic',
        'account_reporting_currency',
    ],
    'data': [
        'views/analytic_line_views.xml',
        'views/analytic_account_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}
