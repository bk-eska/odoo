# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'HR Holidays Turkey',
    'summary': 'Türkiye İzin Alanları',
    'version': '16.0.1.0.1',
    'category': 'Human Resources',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'hr_holidays',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/hr_leave_reason.xml',
        'views/hr_leave_reason_view.xml',
        'views/hr_leave_type_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
