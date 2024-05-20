# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'TLAB Stock Customizations',
    'summary': 'TLAB Stock Customizations',
    'version': '16.0.2.0.0',
    'category': 'Stock',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'LGPL-3',
    'depends': [
        'stock_picking_invoice_link',
    ],
    'data': [
        'security/security.xml',
        'reports/report_stock_traceability.xml',
        'views/stock_move_line_views.xml',
        'views/stock_picking_view.xml',
        'views/stock_scrap_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
