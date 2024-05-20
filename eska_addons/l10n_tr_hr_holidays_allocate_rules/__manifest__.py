# Copyright 2024 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Turkey Leave Auto Allocate Rules',
    'summary': 'Leave auto allocate rules that are used in Turkey',
    'version': '16.0.1.0.0',
    'category': 'Human Resources',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'hr_holidays_allocate_rule',
    ],
    'data': [
        'data/hr_holidays_allocate_rule.xml',
    ],
    'installable': True,
}
