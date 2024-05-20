# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountPartnerLedgerWizard(models.TransientModel):
    _name = 'partner.ledger.reports.wizard'
    _description = 'Partner Ledger Wizard'
    _inherit = "account_financial_report_abstract_wizard"

    date_range_id = fields.Many2one(
        comodel_name="date.range",
        string="Date range"
    )

    date_from = fields.Date(
        string='Start Date',
        required=True,
        default=fields.Date.today().replace(day=1, month=1),
    )

    date_to = fields.Date(
        string='End Date',
        required=True,
        default=fields.Date.context_today,
    )

    target_move = fields.Selection(
        selection=[
            ("posted", "All Posted Entries"),
            ("all", "All Entries"),
        ],
        string="Target Moves",
        required=True,
        default="posted",
    )

    hide_exchange_diff = fields.Boolean(
        string='Hide Exchange Differences',
    )

    receivable_accounts_only = fields.Boolean(
        string='Receivable Accounts',
    )

    payable_accounts_only = fields.Boolean(
        string='Payable Accounts',
    )

    account_ids = fields.Many2many(
        comodel_name="account.account",
        string="Filter accounts"
    )

    partner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Filter partners",
        default=lambda self: self._default_partners(),
        required=True,
    )

    foreign_currency = fields.Boolean(
        string='Show Foreign Currency',
        default=lambda self: self._default_foreign_currency(),
    )

    @api.onchange("partner_ids")
    def onchange_partner_ids(self):
        if self.partner_ids:
            self.receivable_accounts_only = self.payable_accounts_only = True
        else:
            self.receivable_accounts_only = self.payable_accounts_only = False

    @api.onchange("company_id")
    def onchange_company_id(self):
        if (
            self.company_id
            and self.date_range_id.company_id
            and self.date_range_id.company_id != self.company_id
        ):
            self.date_range_id = False
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
        res = {
            "domain": {
                "account_ids": [],
                "partner_ids": [],
                "date_range_id": [],
            }
        }
        if not self.company_id:
            return res
        else:
            res["domain"]["account_ids"] += [
                ("company_id", "=", self.company_id.id)]
            res["domain"]["partner_ids"] += self._get_partner_ids_domain()
            res["domain"]["date_range_id"] += [
                "|",
                ("company_id", "=", self.company_id.id),
                ("company_id", "=", False),
            ]
        return res

    @api.onchange("date_range_id")
    def onchange_date_range_id(self):
        """Handle date range change."""
        if self.date_range_id:
            self.date_from = self.date_range_id.date_start
            self.date_to = self.date_range_id.date_end

    @api.constrains("company_id", "date_range_id")
    def _check_company_id_date_range_id(self):
        for rec in self.sudo():
            if (
                    rec.company_id
                    and rec.date_range_id.company_id
                    and rec.company_id != rec.date_range_id.company_id
            ):
                raise ValidationError(
                    _(
                        "The Company in the Partner Ledger Report Wizard and in "
                        "Date Range must be the same."
                    )
                )

    @api.onchange("receivable_accounts_only", "payable_accounts_only")
    def onchange_type_accounts_only(self):
        if self.receivable_accounts_only or self.payable_accounts_only:
            domain = [("company_id", "=", self.company_id.id)]
            if self.receivable_accounts_only and self.payable_accounts_only:
                domain += [("account_type", "in", ("asset_receivable", "liability_payable"))]
            elif self.receivable_accounts_only:
                domain += [("account_type", "=", "asset_receivable")]
            elif self.payable_accounts_only:
                domain += [("account_type", "=", "liability_payable")]
            self.account_ids = self.env["account.account"].search(domain)
        else:
            self.account_ids = None

    def _default_foreign_currency(self):
        return self.env.user.has_group('base.group_multi_currency')

    def _default_partners(self):
        context = self.env.context
        partners = self.env['res.partner'].browse(context['active_ids'])
        corp_partners = partners.filtered('parent_id')
        partners -= corp_partners
        partners |= corp_partners.mapped('commercial_partner_id')
        return partners.ids

    def _print_report(self, report_type):
        self.ensure_one()
        data = self._prepare_report_partner_ledger()
        if report_type == "xlsx":
            report_name = "account_partner_ledger.report_partner_ledger_xlsx"
        else:
            report_name = "account_partner_ledger.partner_ledger"
        return (
            self.env["ir.actions.reports"].search(
                [("report_name", "=", report_name),
                 ("report_type", "=", report_type)],
                limit=1,
             ).report_action(self, data=data)
        )

    def _prepare_report_partner_ledger(self):
        self.ensure_one()
        return {
            "wizard_id": self.id,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "only_posted_moves": self.target_move == "posted",
            "hide_exchange_diff": self.hide_exchange_diff,
            "company_id": self.company_id.id,
            "partner_ids": self._context["active_ids"],
            "foreign_currency": self.foreign_currency,
            "account_ids": self.account_ids.ids,
            "account_financial_report_lang": self.env.lang,
        }

    def _export(self, report_type):
        return self._print_report(report_type)

    def _get_atr_from_dict(self, obj_id, data, key):
        try:
            return data[obj_id][key]
        except KeyError:
            return data[str(obj_id)][key]
