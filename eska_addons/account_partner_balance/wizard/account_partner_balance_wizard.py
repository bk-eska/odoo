# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PartnerBalanceReportWizard(models.TransientModel):

    _name = "partner.balance.reports.wizard"
    _description = "Partner Balance Report Wizard"
    _inherit = "account_financial_report_abstract_wizard"

    date_at = fields.Date(
        string='Date At',
        required=True,
        default=fields.Date.context_today,
    )

    date_from = fields.Date(
        string="Date From",
    )

    target_move = fields.Selection(
        selection=[
            ("posted", "All Posted Entries"),
            ("all", "All Entries")
        ],
        string="Target Moves",
        required=True,
        default="posted",
    )

    account_ids = fields.Many2many(
        comodel_name="account.account",
        string="Filter accounts",
        domain=[("reconcile", "=", True)],
        required=True,
    )

    hide_account_at_0 = fields.Boolean(
        string="Hide account ending balance at 0",
        default=True,
        help="Use this filter to hide an account or a partner "
        "with an ending balance at 0. "
        "If partners are filtered, "
        "debits and credits totals will not match the trial balance.",
    )

    receivable_accounts_only = fields.Boolean(
        string='Receivable Accounts Only',
    )

    payable_accounts_only = fields.Boolean(
        string='Payable Accounts Only',
    )

    partner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Filter partners",
        default=lambda self: self._default_partners(),
    )

    @api.onchange("company_id")
    def onchange_company_id(self):
        if self.company_id and self.partner_ids:
            self.partner_ids = self.partner_ids.filtered(
                lambda p: p.company_id == self.company_id or not p.company_id
            )
        if self.company_id and self.account_ids:
            if self.receivable_accounts_only or self.payable_accounts_only:
                self.onchange_type_accounts_only()
            else:
                self.account_ids = self.account_ids.filtered(
                    lambda a: a.company_id == self.company_id
                )
        res = {"domain": {"account_ids": [], "partner_ids": []}}
        if not self.company_id:
            return res
        else:
            res["domain"]["account_ids"] += [("company_id", "=", self.company_id.id)]
            res["domain"]["partner_ids"] += self._get_partner_ids_domain()
        return res

    @api.onchange("account_ids")
    def onchange_account_ids(self):
        return {"domain": {"account_ids": [("reconcile", "=", True)]}}

    @api.onchange("receivable_accounts_only", "payable_accounts_only")
    def onchange_type_accounts_only(self):
        domain = [("company_id", "=", self.company_id.id)]
        if self.receivable_accounts_only or self.payable_accounts_only:
            if self.receivable_accounts_only and self.payable_accounts_only:
                domain += [("account_type", "in", ("asset_receivable", "liability_payable"))]
            elif self.receivable_accounts_only:
                domain += [("account_type", "=", "asset_receivable")]
            elif self.payable_accounts_only:
                domain += [("account_type", "=", "liability_payable")]
            self.account_ids = self.env["account.account"].search(domain)
        else:
            self.account_ids = None

    def _print_report(self, report_type):
        self.ensure_one()
        data = self._prepare_report_partner_balance()
        if report_type == "xlsx":
            report_name = "account_partner_balance.report_partner_balance_xlsx"
        else:
            report_name = "account_partner_balance.partner_balance"
        return (
            self.env["ir.actions.reports"]
            .search(
                [("report_name", "=", report_name), ("report_type", "=", report_type)],
                limit=1,
            )
            .report_action(self, data=data)
        )

    def _prepare_report_partner_balance(self):
        self.ensure_one()
        return {
            "wizard_id": self.id,
            "date_at": fields.Date.to_string(self.date_at),
            "date_from": self.date_from or False,
            "only_posted_moves": self.target_move == "posted",
            "hide_account_at_0": self.hide_account_at_0,
            "company_id": self.company_id.id,
            "target_move": self.target_move,
            "account_ids": self.account_ids.ids,
            "partner_ids": self.partner_ids.ids or [],
            "account_financial_report_lang": self.env.lang,
        }

    def _export(self, report_type):
        return self._print_report(report_type)
