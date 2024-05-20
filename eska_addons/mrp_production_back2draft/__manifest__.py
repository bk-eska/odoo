# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'MO to Draft',
    'summary': 'Set cancelled manufacturing orders to draft',
    'version': '16.0.1.0.0',
    'category': 'Manufacturing',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'stock_picking_back2draft',
        'mrp',
    ],
    'data': [
        'views/mrp_production_view.xml',
    ],
    'installable': True,
}
