# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Banks',
    'summary': 'Türkiye Bankalar',
    'version': '16.0.1.0.0',
    'category': 'Localization',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'data/res_bank.xml',
        'views/res_bank_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
