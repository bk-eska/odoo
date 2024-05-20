# Copyright 2024 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'MNG Kargo',
    'summary': 'MNG Kargo',
    'version': '16.0.1.0.0',
    'category': 'Inventory/Delivery',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'delivery',
    ],
    'data': [
        'data/delivery_mng.xml',
        'views/delivery_carrier_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}

