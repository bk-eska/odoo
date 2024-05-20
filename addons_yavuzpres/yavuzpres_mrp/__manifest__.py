# Copyright 2023 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Yavuzpres MRP Customization',
    'summary': 'Yavuzpres MRP Customization',
    'version': '16.0.1.0.0',
    'category': 'Manufacturing',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'mrp',
    ],
    'data': [
        'security/security.xml',
        'views/mrp_production_view.xml',
        'views/mrp_bom_view.xml',
        'views/stock_picking_type_view.xml',
        'reports/mrp_production_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}
