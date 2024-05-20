# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "HR Holidays Force Use Whole Week",
    "summary": "This module forces to use the whole week if the leave start day is Monday and the end day is Friday.",
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
