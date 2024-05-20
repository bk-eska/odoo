# Copyright 2024 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Otto Integration",
    "summary": "Otto Integration",
    "version": "16.0.1.0.0",
    "category": "Sale",
    "website": "https://eska.biz",
    "author": "Eska",
    "license": "AGPL-3",
    "depends": [
        "sale",
    ],
    "data": [
        'data/data.xml',
        'data/ir_cron.xml',
        'views/res_company_view.xml',
        'views/sale_order_view.xml',
    ],
    "auto_install": False,
    "installable": True,
}
