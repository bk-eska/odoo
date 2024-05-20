# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": 'Account Invoice Add Sale Line',
    "summary": 'Adds invoice line from sale lines',
    "version": "16.0.1.0.0",
    "category": 'Sale',
    "author": 'Eska',
    "website": 'http://www.eskayazilim.com.tr',
    "license": 'AGPL-3',
    "depends": [
        'sale',
    ],
    "data": [
        'security/ir.model.access.csv',
        'wizard/invoice_add_sale_line_wizard_view.xml',
        'views/account_move_view.xml',
        'views/sale_order_line_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
