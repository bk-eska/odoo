# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Base Automation Contract Crm',
    'summary': 'This module adds contract to crm and creates crm with an automated action',
    'version': '14.0.1.0.0',
    'category': 'Contract',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'base_automation',
        'contract',
        'crm',
    ],
    'data': [
        'data/base_automation_data.xml',
        'views/crm_lead_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}