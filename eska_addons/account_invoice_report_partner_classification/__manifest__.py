# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Invoice Report Partner Classifiation",
    "summary": "Account Invoice Report Partner Classifiation",
    "version": "16.0.1.0.0",
    "category": "Account",
    "website": "http://www.eskayazilim.com.tr",
    "author": "Eska",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "account",
        "partner_classification",
    ],
    "data": [
        'reports/account_invoice_report_view.xml'
    ]
}
