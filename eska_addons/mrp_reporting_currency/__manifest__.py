# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'MRP BOM Structure Reporting Currency',
    'summary': 'MRP BOM Structure Reporting Currency',
    'version': '16.0.1.0.0',
    'category': 'MRP',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'mrp_bom_report_hook',
        'stock_reporting_currency',
    ],
    'data': [
        'reports/mrp_report_bom_structure.xml',
        'views/mrp_workcenter_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mrp_reporting_currency/static/src/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
}
