# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "TLab Maintenance Customization",
    "summary": "TLab Maintenance Customization",
    "version": "16.0.1.0.0",
    "category": "Manufacturing/Maintenance",
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'maintenance',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_views.xml',
    ],
    'installable': True,
}
