# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Check Voucher',
    'summary': 'Account Check Voucher',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account_check',
    ],
    'data': [
        'reports/report_check_voucher.xml',
        'views/reports.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
