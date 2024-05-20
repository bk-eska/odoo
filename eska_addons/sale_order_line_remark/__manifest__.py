# Copyright 2024 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale Order Line Remark',
    'summary': 'Sale Order',
    'version': '16.0.1.0.0',
    'category': 'Sale',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale',
    ],
    'data': [
        'reports/sale_report_templates.xml',
        'views/sale_order_line_views.xml',
        'reports/sale_portal_templates.xml',
    ],
    'installable': True,
}
