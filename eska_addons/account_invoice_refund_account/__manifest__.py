# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Invoice Refund Account",
    "summary": "Account Invoice Refund Account",
    "version": "16.0.1.0.0",
    "category": "Product",
    "website": "http://www.eskayazilim.com.tr",
    "author": "Eska",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": False,
    "depends": [
        "account",
    ],
    "data": [
        "views/product_category_view.xml",
        "views/product_template_view.xml"
    ]
}
