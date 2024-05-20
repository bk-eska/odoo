# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Stock Ledger Report",
    "version": "16.0.1.0.0",
    "summary": "Stock Ledger Report",
    "description": 'Stock Ledger Report',
    "author": 'Eska',
    "website": 'http://www.eskayazilim.com.tr',
    "license": 'AGPL-3',
    "depends": [
        'base',
        'report_xlsx',
        'product',
        'stock',
    ],
    "category": "Stock",
    'data': [
        'security/ir.model.access.csv',
        'reports/reports.xml',
        "wizard/stock_ledger_report_wizard_view.xml",
    ],
    'installable': True,
    'auto_install': False,
}
