# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Accounting Document Fields Enterprise',
    'summary': 'Türkiye Muhasebe Belge Alanları Kurumsal',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account_accountant',
        'l10n_tr_account_document',
    ],
    'data': [
        'views/account_bank_statement_line_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
