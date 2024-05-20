# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale Price From Profit Rate',
    'summary': 'Sale Price From Profit Rate',
    'version': '16.0.1.0.0',
    'category': 'Sale',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale_margin',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_calculate_price_wizard_view.xml',
        'views/product_category_views.xml',
        'views/product_template_views.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
