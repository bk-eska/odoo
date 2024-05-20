# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Work Schedule',
    'summary': 'Türkiye Çalışma Saatleri',
    'version': '16.0.1.0.0',
    'category': 'Human Resources',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'resource',
    ],
    'data': [
        'data/resource_calendar.xml',
    ],
    'installable': True,
    'auto_install': False,
    'external_dependencies': {
        'python': ['openupgradelib']
    },
    'pre_init_hook': 'pre_init_hook',
}
