# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Currency Rate Type',
    'summary': 'Use different currency rate types',
    'version': '16.0.1.0.0',
    'category': 'Base',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_currency_rate_type_view.xml',
        'views/res_currency_rate_view.xml',
        'views/res_currency_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}

