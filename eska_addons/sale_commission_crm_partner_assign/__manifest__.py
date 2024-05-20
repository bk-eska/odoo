# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale Commission Assign Partner',
    'summary': 'Adds commission to contracts as',
    'version': '16.0.1.0.0',
    'category': 'Sales Management',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'commission',
        'website_crm_partner_assign',
    ],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
