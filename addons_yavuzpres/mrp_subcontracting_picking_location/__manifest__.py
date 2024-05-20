# Copyright 2024 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'MRP Subcontracting Picking Location',
    'summary': 'MRP Subcontracting Picking Location',
    'version': '16.0.1.0.0',
    'category': 'MRP',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'mrp_subcontracting',
    ],
    'data': [
        'views/stock_picking_type_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
