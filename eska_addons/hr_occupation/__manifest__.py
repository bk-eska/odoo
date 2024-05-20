# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Occupations',
    'summary': 'Occupations',
    'version': '16.0.1.0.0',
    'category': 'HR',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'hr',
    ],
    'data': [
        'views/hr_occupation_views.xml',
        'security/ir.model.access.csv',
        'views/hr_job_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
