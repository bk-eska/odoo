# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'MRP Production Date',
    'summary': 'Updates the production date of the lot when the manufacturing order is marked as done',
    'version': '16.0.1.0.0',
    'category': 'Stock',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'stock_production_date',
        'mrp',
    ],
    'data': [
        'views/mrp_production_view.xml',
    ],
    'installable': True,
}
