# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Base Automation Contract Email',
    'summary': 'This module adds an automated action that will send reminder email as contracts close to ending',
    'version': '14.0.1.0.0',
    'category': 'Contract',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'base_automation',
        'contract',
    ],
    'data': [
        'data/mail_template_data.xml',
        'data/base_automation_data.xml',
    ],
    'installable': True,
    'auto_install': False,
}