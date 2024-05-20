# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Delivery Fields',
    'summary': 'Türkiye Teslimat Alanları',
    'version': '16.0.2.0.0',
    'category': 'Localization',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'delivery',
    ],
    'data': [
        'views/report_deliveryslip.xml',
        'views/res_partner_view.xml',
        'views/stock_picking_view.xml',
        'views/stock_package_type_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'external_dependencies': {
        'python': ['openupgradelib']
    },
    'pre_init_hook': 'pre_init_hook',
}
