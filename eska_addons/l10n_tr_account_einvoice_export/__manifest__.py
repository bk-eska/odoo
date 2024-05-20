# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'E-Fatura İhracat',
    'summary': 'Türkiye E-Fatura İhracat',
    'version': '16.0.4.0.0',
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account_currency_rate',
        'l10n_tr_account_einvoice_delivery',
        'partner_contact_personal_info',
        'partner_contact_passport',
    ],
    'data': [
        'views/account_fiscal_position_view.xml',
        'views/account_move_view.xml',
        'views/product_template_view.xml',
        'data/l10n_tr_einvoice_postbox.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
