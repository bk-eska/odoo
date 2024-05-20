# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Panorama Sale',
    'summary': 'Panorama Sale Customizations',
    'version': '16.0.1.0.0',
    'category': 'Sale',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale_order_archive',
    ],
    'data': [
        'views/sale_order_view.xml',
        'views/sale_portal_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}
