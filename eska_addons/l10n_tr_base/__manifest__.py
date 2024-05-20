# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Accounting Base',
    'summary': 'Türkiye Muhasebe Yerelleştirmesi Temeli',
    'version': '16.0.1.0.0',
    'category': 'Accounting/Localizations/Account Charts',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_fiscal_position_view.xml',
        'views/account_tax_group_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
