# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Yavuzpres Sale Customization',
    'summary': 'Yavuzpres Sale Customization',
    'version': '16.0.1.0.0',
    'category': 'Sale',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account_invoice_add_sale_line',
        'sale_stock',
    ],
    'data': [
        'views/sale_order_line_view.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
}
