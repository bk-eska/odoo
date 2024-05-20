# Copyright 2018 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Hr Analytic Base",
    'summary': 'Base module for advanced analytics in HR applications',
    "version": "16.0.1.0.0",
    "category": "HR",
    "author": "Eska",
    "website": "http://www.eskayazilim.com.tr",
    "license": "AGPL-3",
    "auto_install": False,
    "depends": [
         "hr",
         "analytic",
    ],
    "data": [
         "views/hr_department_view.xml",
         "views/hr_employee_view.xml",
    ],
    "installable": True,
}

