# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'HR Holidays Limit Leave Count',
    'summary': 'This module enables to setting a limit for the maximum leave count for monthly or yearly',
    'version': '16.0.1.0.0',
    'category': 'HR',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'hr_holidays',
    ],
    'data': [
        'views/hr_leave_type_views.xml',
    ],
    'installable': True,
}
