# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Currency Rate',
    'summary': 'See currency rate on accounting documents',
    'version': '16.0.2.0.0',
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'currency_rate_precision',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/account_currency_rate_security.xml',
        'wizard/account_payment_register_view.xml',
        'wizard/account_convert_currency_view.xml',
        'views/account_move_view.xml',
        'views/account_payment_view.xml',
        'views/res_config_settings_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'external_dependencies': {
        'python': ['openupgradelib']
    },
    'pre_init_hook': 'pre_init_hook',
}
