# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Reflection Account',
    'summary': 'Türkiye Yansıtma Hesabı',
    'version': '16.0.1.0.0',
    'category': 'Localization',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'OPL-1',
    'depends': [
        'account_auto_transfer',
    ],
    'data': [
        'views/account_account_view.xml',
        'views/account_transfer_model_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
