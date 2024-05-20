# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Currency Rate Update Again',
    'summary': 'Currency Rate Update Again',
    'version': '16.0.1.0.0',
    'category': 'Financial Management/Configuration',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'currency_rate_update',
    ],
    'data': [
        "data/cron.xml",
    ],
    'installable': True,
    'auto_install': True,
}
