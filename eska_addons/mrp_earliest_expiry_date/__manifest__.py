# Copyright 2022 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'MRP Production Earliest Expire Date',
    'summary': 'MRP Customizations',
    'version': '16.0.1.0.0',
    'category': 'Manufacturing',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'LGPL-3',
    'depends': [
        'mrp',
    ],
    'data': [
        'reports/mrp_production_templates.xml',
        'views/mrp_production_view.xml'
    ],
    'installable': True,
    'auto_install': False,
}
