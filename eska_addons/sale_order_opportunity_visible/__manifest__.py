# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Show Opportunity On The Sale View",
    'summary': 'This module shows opportunity fields on the sale view',
    'author': "Eska",
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'category': 'sale',
    'version': '16.0.1.0.0',
    'depends': [
        'sale_crm',
    ],
    'data': [
        'views/sale_crm_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'external_dependencies': {
        'python': ['openupgradelib']
    },
    'pre_init_hook': 'pre_init_hook',
}
