# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'YavuzPres Sale MRP Intercompany',
    'summary': 'Create intercompany manufacturing orders from sale orders',
    'version': '16.0.1.0.0',
    'category': 'Sale',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale_mrp',
        'yavuzpres_mrp',
    ],
    'data': [
        'views/mrp_production_view.xml',
        'views/res_company_view.xml',
        'views/sale_order_view.xml',
        'views/stock_picking_type_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
