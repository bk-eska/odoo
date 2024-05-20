# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Accounting Document Fields',
    'summary': 'Türkiye Muhasebe Belge Alanları',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'l10n_tr_base',
        'l10n_tr_document',
    ],
    'data': [
        'wizard/account_payment_register_view.xml',
        'views/account_move_view.xml',
        'views/account_journal_view.xml',
        'views/account_payment_view.xml',
    ],
    'installable': True,
    'auto_install': True,
    'external_dependencies': {
        'python': ['openupgradelib']
    },
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
}
