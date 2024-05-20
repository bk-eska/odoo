# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Purchase Report Hide Zero Quantity',
    'summary': 'Purchase Report Hide Zero',
    'version': '16.0.1.0.0',
    'category': 'Purchase',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
    ],
    'data': [
        'reports/purchase_order_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}
