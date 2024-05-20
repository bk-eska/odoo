# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Contact Passport",
    "summary": "Add passport information to contacts",
    "version": "16.0.1.0.1",
    "category": "Customer Relationship Management",
    "author": "Eska",
    "website": "http://www.eskayazilim.com.tr",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": False,
    "depends": [
        "base",
    ],
    "data": [
        'security/ir.model.access.csv',
        "views/res_partner_views.xml",
    ],
}
