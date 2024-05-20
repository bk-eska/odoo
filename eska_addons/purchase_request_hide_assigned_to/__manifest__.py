# Copyright 2021 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Request Hide Assigned To',
    'summary': 'Hide assigned to field in purchase requests',
    'version': '16.0.1.0.0',
    'category': 'Contract Management',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'purchase_request',
    ],
    'data': [
        'views/purchase_request_view.xml',
        'views/purchase_request_line_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
