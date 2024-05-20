# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Account Vat Return Report",
    "version": "16.0.1.0.0",
    "summary": "Account Vat Return Report",
    "description": "Account Vat Return Report",
    "author": 'Eska',
    "website": 'http://www.eskayazilim.com.tr',
    "license": 'AGPL-3',
    "category": "Accounting",
    "depends": [
        "account",
        "report_xlsx",
        "purchase",
        "date_range",
        "l10n_tr_account_document",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/reports.xml",
        "wizard/account_vat_report_wizard_view.xml",
    ],
    "installable": True,
}
