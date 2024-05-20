# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Contact Personal Information",
    "summary": "Add personal information fields to contacts",
    "version": "16.0.2.0.0",
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
        "views/res_partner_views.xml",
    ],
    'external_dependencies': {
        'python': ['openupgradelib']
    },
    'pre_init_hook': 'pre_init_hook',
}
