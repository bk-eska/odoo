# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Accounting',
    'summary': 'Türkiye Muhasebe Yerelleştirmesi',
    'version': '16.0.2.0.0',
    'category': 'Accounting/Localizations/Account Charts',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'l10n_tr_base',
    ],
    'data': [
        'data/l10n_tr_tax_type_data.xml',
        'data/account_tax_group_data.xml',
        'data/account_chart_template_data.xml',
        'data/account_account_template_data.xml',
        'data/account_tax_template_data.xml',
        'data/account_fiscal_position_template_data.xml',
        'data/account_fiscal_position_account_template_data.xml',
        'data/account_fiscal_position_tax_template_data.xml',
        'data/account_group_template_data.xml',
        'data/account_chart_template_configure_data.xml',
    ],
    'installable': True,
    'auto_install': False,
}
