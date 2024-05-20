# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Pre-numbered Invoices',
    'summary': 'Use pre-numbered invoice documents.',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'l10n_tr_account_document',
    ],
    'data': [
        'views/account_journal_view.xml',
        'views/account_move_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
