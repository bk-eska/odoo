# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Sale Final Customer",
    "version": "16.0.1.0.0",
    "summary": "Adding a final customer field to the Sale Order",
    "description": "Adding a final customer field to the Sale Order",
    "author": 'Eska',
    "website": 'http://www.eskayazilim.com.tr',
    "license": 'AGPL-3',
    "category": "CRM",
    "depends": [
        "sale",
    ],
    "data": [
        'views/sale_order_views.xml',
    ],
    "installable": True,
}
