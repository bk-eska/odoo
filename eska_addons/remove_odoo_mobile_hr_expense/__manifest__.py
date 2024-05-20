# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Remove Odoo Mobile HR Expense",
    'summary': 'Remove Odoo Mobile on HR Expense',
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "category": "Maintenance",
    "author": "Eska",
    "website": "http://www.eskayazilim.com.tr",
    "license": "AGPL-3",
    "depends": [
        "hr_expense",
    ],
    "data": [
        'views/hr_expense_views.xml',
    ],
    "installable": True,
}
