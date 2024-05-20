# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Occupation Codes',
    'summary': 'Türkiye Meslek Kodları',
    'version': '16.0.1.0.0',
    'category': 'HR',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'hr_occupation',
    ],
    'data': [
        'data/hr_occupation_data.xml',
    ],
    'installable': True,
    'auto_install': True,
}
