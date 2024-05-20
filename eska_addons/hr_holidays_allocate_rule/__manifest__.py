# Copyright 2024 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Auto Allocate Leaves',
    'summary': 'Allocate leaves automatically',
    'version': '16.0.1.0.1',
    'category': 'Human Resources',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'hr_holidays',
        'hr_employee_service',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_view.xml',
        'views/hr_holidays_allocate_rule_view.xml',
        'data/hr_holidays_auto_allocate_data.xml',
    ],
    'installable': True,
}
