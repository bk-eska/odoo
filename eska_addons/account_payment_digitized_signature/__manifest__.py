# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "account_payment_digitized_signature",
    "version": "16.0",
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    "depends": [
        "account"
    ],
    "data": [
        "views/account_sign_inherit.xml",
        "reports/account_digitized_signature_pdf_inherit.xml",
    ],
    "auto_install": False,
}
