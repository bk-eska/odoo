# Author: Damien Crier
# Author: Julien Coux
# Copyright 2016 Camptocamp SA
# Copyright 2020 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2021 Tecnativa - João Marques
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Financial Reports",
    "version": "16.0.1.3.9",
    "category": "Reporting",
    "summary": "OCA Financial Reports",
    "author": "Camptocamp SA,"
    "initOS GmbH,"
    "redCOR AG,"
    "ForgeFlow,"
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-financial-reporting",
    "depends": ["account", "date_range", "report_xlsx"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/aged_partner_balance_wizard_view.xml",
        "wizard/general_ledger_wizard_view.xml",
        "wizard/journal_ledger_wizard_view.xml",
        "wizard/open_items_wizard_view.xml",
        "wizard/trial_balance_wizard_view.xml",
        "wizard/vat_report_wizard_view.xml",
        "menuitems.xml",
        "reports.xml",
        "reports/templates/layouts.xml",
        "reports/templates/aged_partner_balance.xml",
        "reports/templates/general_ledger.xml",
        "reports/templates/journal_ledger.xml",
        "reports/templates/open_items.xml",
        "reports/templates/trial_balance.xml",
        "reports/templates/vat_report.xml",
        "view/account_view.xml",
        "view/report_general_ledger.xml",
        "view/report_journal_ledger.xml",
        "view/report_trial_balance.xml",
        "view/report_open_items.xml",
        "view/report_aged_partner_balance.xml",
        "view/report_vat_report.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "account_financial_report/static/src/js/*",
            "account_financial_report/static/src/xml/**/*",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "AGPL-3",
}
