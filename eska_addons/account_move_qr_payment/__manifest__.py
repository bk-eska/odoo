# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Move QR Payment',
    'summary': 'Adds QR Code to invoices for payments',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'LGPL-3',
    'depends': [
        'account',
    ],
    'external_dependencies': {
        'python': [
            'qrcode[PIL]',
        ],
    },
    'data': [
        'reports/report_invoice.xml',
    ],
    'installable': True,
    'auto_install': False,
}
