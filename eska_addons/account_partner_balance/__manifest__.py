# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Partner Balance List',
    'summary': 'Partner balance',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account_financial_report',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/account_partner_balance_wizard.xml',
        'views/menu.xml',
        'reports/partner_balance_templates.xml',
        'reports/partner_balance.xml',
    ],
    'installable': True,
}
