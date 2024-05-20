# Copyright 2017 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Central Bank of the Republic of Turkey (TCMB) Currency Provider',
    'summary': 'Türkiye Cumhuriyeti Merkez Bankası (TCMB) Kur Sağlayıcısı',
    'version': '16.0.1.0.0',
    'category': 'Financial Management/Configuration',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'currency_rate_update',
        'currency_rate_type',
    ],
    'data': [
        'views/res_currency_rate_provider.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
