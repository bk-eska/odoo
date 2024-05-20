# Copyright 2017 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Leave Types',
    'summary': 'Türkiye İzin Türleri',
    'version': '16.0.1.0.0',
    'category': 'Human Resources',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'hr_holidays',
        'hr_holidays_limit_per_request'
    ],
    'data': [
        'data/mail_data.xml',
        'data/hr_leave_type.xml',
    ],
    'installable': True,
    'auto_install': False,
}
