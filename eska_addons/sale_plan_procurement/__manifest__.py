# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale Plan Procurement',
    'summary': 'Sale procurement planning',
    'version': '16.0.1.0.0',
    'category': 'Sale',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale_purchase_stock',
        'sale_stock_margin',
        'purchase_requisition_stock',
        'sale_price_from_profit_rate',
        'sale_order_line_remark',
        'purchase_order_line_remark',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_purchase_generate_wizard_views.xml',
        'reports/purchase_report_templates.xml',
        'reports/sale_report_templates.xml',
        'views/product_category_views.xml',
        'views/product_template_views.xml',
        'views/res_partner_views.xml',
        'views/sale_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}