# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Mali Yıl Kapanış',
    'summary': 'Muhasebe Mali Yıl Kapanış',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account_fiscal_year_closing',
    ],
    'data': [
        'data/account_fiscalyear_closing_template_data.xml',
        'data/account_fiscalyear_closing_config_template_data.xml',
        'data/account_fiscalyear_closing_type_template_data.xml',
        'data/account_fiscalyear_closing_mapping_template_data.xml'
    ],
    'installable': True,
    'application': False,
}
