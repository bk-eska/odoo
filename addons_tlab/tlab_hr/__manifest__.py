# Copyright 2024 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "TLab Skills Management",
    "summary": "Manage skills, knowledge and resume of your employees",
    "version": "16.0.1.0.0",
    "category": 'Human Resources/Employees',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'hr_skills',
    ],
    'data': [
        'views/hr_views.xml',
        'reports/hr_employee_skill_report_views.xml',
    ],
    'installable': True,
}
