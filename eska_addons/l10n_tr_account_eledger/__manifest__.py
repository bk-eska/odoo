# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey E-Ledger',
    'summary': 'E-Ledger implementation',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'l10n_tr_account_document',
        'l10n_tr_account_sequence',
        'iap_company_account',
    ],
    'data': [
        'views/date_range_view.xml',
    ],
    'installable': True,
    'application': True,
}
