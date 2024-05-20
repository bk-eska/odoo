# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Stock Production Date',
    'summary': 'Adds production date to detailed operations.',
    'version': '16.0.1.0.0',
    'category': 'Stock',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'product_expiry'
    ],
    'data': [
        'views/stock_move_views.xml',
        'views/production_lot_views.xml',
        'reports/report_deliveryslip.xml',
    ],
    'installable': True,
}
