# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Partner ID Fields',
    'summary': 'Türkiye Kimlik Bilgileri',
    'version': '16.0.1.0.0',
    'category': 'Base',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'partner_contact_personal_info',
    ],
    'data': [
        'views/res_partner_view.xml'
    ],
    'installable': True,
    'auto_install': False,
}
