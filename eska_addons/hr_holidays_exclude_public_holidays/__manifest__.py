# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "HR Holidays Exclude Public Holidays",
    "summary": "This module excludes public holidays in calculation of leave duration days",
    "version": "16.0.1.0.0",
    "category": "Human Resources",
    "website": "http://www.eskayazilim.com.tr",
    "author": "ESKA",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "hr_holidays",
    ],
    "data": [
        'views/hr_leave_type_view.xml',
    ]
}
