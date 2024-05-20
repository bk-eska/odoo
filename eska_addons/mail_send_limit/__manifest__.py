# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Mail Send Limit',
    'summary': 'Set a limit for sending emails',
    'version': '16.0.1.0.0',
    'category': 'Mail',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends' : [
        'mail',
    ],
    'data': [
        'views/res_config_settings.xml',
    ],
    'installable': True,
    'auto_install': False,
}
