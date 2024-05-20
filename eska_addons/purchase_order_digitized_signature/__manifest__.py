# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Purchase Order Digitized Signature',
    'summary': 'Purchase Order Digitized Signature',
    'version': '16.0.1.0.0',
    'category': 'Purchase',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
    ],
    'data': [
        'views/purchase_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
