# Copyright 2024 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Maintenance Equipment Assignment",
    "summary": "Maintenance Equipment Assignment",
    "version": "16.0.1.0.0",
    "category": "Manufacturing/Maintenance",
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'hr_maintenance',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_views.xml',
        'report/equipment_assign_report.xml',
    ],
    'installable': True,
}
