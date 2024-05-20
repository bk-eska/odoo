# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class PartnerLedgerReport(models.AbstractModel):
    _name = "reports.account_partner_ledger.partner_ledger"
    _description = "Partner Ledger Report"

    def _get_accounts_data(self, account_ids):
        accounts = self.env["account.account"].browse(account_ids)
        accounts_data = {}
        for account in accounts:
            accounts_data.update(
                {
                    account.id: {
                        "id": account.id,
                        "code": account.code,
                        "name": account.name,
                    }
                }
            )
        return accounts_data

    def _get_currencies_data(self, currency_ids):
        currencies = self.env["res.currency"].browse(currency_ids)
        currencies_data = {}
        for currency in currencies:
            currencies_data.update(
                {
                    currency.id: {
                        "id": currency.id,
                        "name": currency.name,
                        "currency_id": currency,
                    }
                }
            )
        return currencies_data

    def _get_journals_data(self, journals_ids):
        journals = self.env["account.journal"].browse(journals_ids)
        journals_data = {}
        for journal in journals:
            journals_data.update({journal.id: {"id": journal.id, "code": journal.code}})
        return journals_data

    def _get_initial_balances_bs_ml_domain(
        self, account_ids, company_id, date_from, base_domain, acc_prt=False
    ):
        accounts_domain = [
            ("company_id", "=", company_id),
            ("include_initial_balance", "=", True),
        ]
        if account_ids:
            accounts_domain += [("id", "in", account_ids)]
        domain = []
        domain += base_domain
        domain += [("date", "<", date_from)]
        accounts = self.env["account.account"].search(accounts_domain)
        domain += [("account_id", "in", accounts.ids)]
        if acc_prt:
            domain += [("account_type", "in", ["asset_receivable", "liability_payable"])]
        return domain

    def _get_initial_balance_data(
        self,
        account_ids,
        partner_ids,
        company_id,
        date_from,
        foreign_currency,
        only_posted_moves,
        hide_exchange_diff,
    ):
        base_domain = []
        if company_id:
            base_domain += [("company_id", "=", company_id)]
        if partner_ids:
            base_domain += [("partner_id", "in", partner_ids)]
        if only_posted_moves:
            base_domain += [("move_id.state", "=", "posted")]
        else:
            base_domain += [("move_id.state", "in", ["posted", "draft"])]
        if hide_exchange_diff:
            base_domain += [("amount_currency", "!=", 0.0)]

        initial_domain_acc_prt = self._get_initial_balances_bs_ml_domain(
            account_ids, company_id, date_from, base_domain, acc_prt=True
        )
        if foreign_currency:
            grouping = ["partner_id", "currency_id"]
        else:
            grouping = ["partner_id"]

        gl_initial_acc_prt = self.env["account.move.line"].read_group(
            domain=initial_domain_acc_prt,
            fields=[
                "currency_id",
                "partner_id",
                "debit",
                "credit",
                "balance",
                "amount_currency:sum",
            ],
            groupby=grouping,
            lazy=False,
        )
        company = self.env["res.company"].browse(company_id)
        gen_ld_data = {}
        currency_ids = set()
        partners_data = {}
        if gl_initial_acc_prt:
            for gl in gl_initial_acc_prt:
                prt_id = gl["partner_id"][0]
                prt_name = gl["partner_id"][1]
                partners_data.update({prt_id: {"id": prt_id, "name": prt_name}})
                if foreign_currency and gl["currency_id"] and gl["currency_id"][0]:
                    cur_id = gl["currency_id"][0]
                    cur_name = str(gl["currency_id"][1])
                else:
                    cur_id = company.currency_id.id
                    cur_name = company.currency_id.name
                if cur_id not in currency_ids:
                    currency_ids.add(cur_id)
                if prt_id not in gen_ld_data:
                    gen_ld_data[prt_id] = {}
                    gen_ld_data[prt_id]["id"] = prt_id
                gen_ld_data[prt_id][cur_id] = {}
                gen_ld_data[prt_id][cur_id]["id"] = cur_id
                gen_ld_data[prt_id][cur_id]["name"] = cur_name
                gen_ld_data[prt_id][cur_id]["init_bal"] = {}
                gen_ld_data[prt_id][cur_id]["init_bal"]["credit"] = gl["credit"]
                gen_ld_data[prt_id][cur_id]["init_bal"]["debit"] = gl["debit"]
                gen_ld_data[prt_id][cur_id]["init_bal"]["balance"] = gl["balance"]
                gen_ld_data[prt_id][cur_id]["fin_bal"] = {}
                gen_ld_data[prt_id][cur_id]["fin_bal"]["credit"] = gl["credit"]
                gen_ld_data[prt_id][cur_id]["fin_bal"]["debit"] = gl["debit"]
                gen_ld_data[prt_id][cur_id]["fin_bal"]["balance"] = gl["balance"]
                gen_ld_data[prt_id][cur_id]["init_bal"]["bal_curr"] = gl[
                    "amount_currency"
                ]
                gen_ld_data[prt_id][cur_id]["fin_bal"]["bal_curr"] = gl[
                    "amount_currency"
                ]
        return gen_ld_data, partners_data, currency_ids

    @api.model
    def _get_move_line_data(self, move_line):
        if move_line["name"] and move_line["ref"]:
            ref = "%s - %s" % (move_line["name"], move_line["ref"])
        elif move_line["name"]:
            ref = move_line["name"]
        elif move_line["ref"]:
            ref = move_line["ref"]
        else:
            ref = ""
        move_line_data = {
            "id": move_line["id"],
            "date": move_line["date"],
            "date_maturity": move_line["date_maturity"],
            "entry": move_line["move_id"][1],
            "entry_id": move_line["move_id"][0],
            "account_id": move_line["account_id"][0],
            "journal_id": move_line["journal_id"][0],
            "partner_id": move_line["partner_id"][0]
            if move_line["partner_id"]
            else False,
            "partner_name": move_line["partner_id"][1]
            if move_line["partner_id"]
            else "",
            "ref": ref,
            "debit": move_line["debit"],
            "credit": move_line["credit"],
            "balance": move_line["balance"],
            "amount_currency": move_line["amount_currency"],
            "bal_curr": move_line["amount_currency"],
            "currency_id": move_line["currency_id"],
            "currency_rate": 0.0 if not move_line["amount_currency"]
            else abs((move_line["debit"]+move_line["credit"])
                     /move_line["amount_currency"]),
        }
        return move_line_data

    @api.model
    def _get_period_domain(
        self,
        account_ids,
        partner_ids,
        company_id,
        only_posted_moves,
        hide_exchange_diff,
        date_to,
        date_from,
    ):
        domain = [
            ("display_type", "not in", ["line_note", "line_section"]),
            ("date", ">=", date_from),
            ("date", "<=", date_to),
        ]
        if account_ids:
            domain += [("account_id", "in", account_ids)]
        if company_id:
            domain += [("company_id", "=", company_id)]
        if partner_ids:
            domain += [("partner_id", "in", partner_ids)]
        if only_posted_moves:
            domain += [("move_id.state", "=", "posted")]
        else:
            domain += [("move_id.state", "in", ["posted", "draft"])]
        if hide_exchange_diff:
            domain += [("amount_currency", "!=", 0.0)]
        return domain

    def _initialize_currency(self, gen_ld_data, prt_id, cur_id, cur_name, foreign_currency):
        gen_ld_data[prt_id][cur_id] = {}
        gen_ld_data[prt_id][cur_id]["id"] = cur_id
        gen_ld_data[prt_id][cur_id]["name"] = cur_name
        gen_ld_data[prt_id][cur_id]["init_bal"] = {}
        gen_ld_data[prt_id][cur_id]["init_bal"]["balance"] = 0.0
        gen_ld_data[prt_id][cur_id]["init_bal"]["credit"] = 0.0
        gen_ld_data[prt_id][cur_id]["init_bal"]["debit"] = 0.0
        gen_ld_data[prt_id][cur_id]["fin_bal"] = {}
        gen_ld_data[prt_id][cur_id]["fin_bal"]["credit"] = 0.0
        gen_ld_data[prt_id][cur_id]["fin_bal"]["debit"] = 0.0
        gen_ld_data[prt_id][cur_id]["fin_bal"]["balance"] = 0.0
        gen_ld_data[prt_id][cur_id]["init_bal"]["bal_curr"] = 0.0
        gen_ld_data[prt_id][cur_id]["fin_bal"]["bal_curr"] = 0.0
        return gen_ld_data

    def _get_period_ml_data(
        self,
        account_ids,
        partner_ids,
        company_id,
        foreign_currency,
        only_posted_moves,
        hide_exchange_diff,
        date_from,
        date_to,
        partners_data,
        gen_ld_data,
        currency_ids,
    ):
        domain = self._get_period_domain(
            account_ids,
            partner_ids,
            company_id,
            only_posted_moves,
            hide_exchange_diff,
            date_to,
            date_from,
        )
        ml_fields = [
            "id",
            "name",
            "date",
            "date_maturity",
            "move_id",
            "journal_id",
            "account_id",
            "partner_id",
            "debit",
            "credit",
            "balance",
            "currency_id",
            "tax_ids",
            "amount_currency",
            "ref",
        ]
        move_lines = self.env["account.move.line"].search_read(
            domain=domain, fields=ml_fields, order="date,move_name"
        )
        journal_ids = set()
        for move_line in move_lines:
            journal_ids.add(move_line["journal_id"][0])
            ml_id = move_line["id"]
            prt_id = move_line["partner_id"][0]
            partner_name = move_line["partner_id"][1]
            partners_data.update({prt_id: {"id": prt_id, "name": partner_name}})
            if prt_id not in gen_ld_data:
                gen_ld_data[prt_id] = {}
                gen_ld_data[prt_id]["id"] = prt_id
            if foreign_currency and move_line["currency_id"]:
                cur_id = move_line["currency_id"][0]
                cur_name = move_line["currency_id"][1]
            else:
                company = self.env["res.company"].browse(company_id)
                cur_id = company.currency_id.id
                cur_name = company.currency_id.name
            if cur_id not in currency_ids:
                currency_ids.add(cur_id)
            if cur_id not in gen_ld_data[prt_id]:
                gen_ld_data = self._initialize_currency(
                    gen_ld_data, prt_id, cur_id, cur_name, foreign_currency
                )
            gen_ld_data[prt_id][cur_id][ml_id] = self._get_move_line_data(move_line)
            gen_ld_data[prt_id][cur_id]["fin_bal"]["credit"] += move_line["credit"]
            gen_ld_data[prt_id][cur_id]["fin_bal"]["debit"] += move_line["debit"]
            gen_ld_data[prt_id][cur_id]["fin_bal"]["balance"] += move_line[
                "balance"
            ]
            if foreign_currency:
                gen_ld_data[prt_id][cur_id]["fin_bal"]["bal_curr"] += move_line[
                    "amount_currency"
                ]
        journals_data = self._get_journals_data(list(journal_ids))
        currencies_data = self._get_currencies_data(list(currency_ids))
        accounts_data = self._get_accounts_data(list(account_ids))
        return (
            gen_ld_data,
            currencies_data,
            accounts_data,
            partners_data,
            journals_data,
        )

    @api.model
    def _recalculate_cumul_balance(self, move_lines, last_cumul_balance, last_cumul_curr_balance):
        for move_line in move_lines:
            move_line["balance"] += last_cumul_balance
            move_line["bal_curr"] += last_cumul_curr_balance
            last_cumul_balance = move_line["balance"]
            last_cumul_curr_balance = move_line["bal_curr"]
        return move_lines

    @api.model
    def _create_partner_ledger(self, gen_led_data, partners_data, currencies_data):
        partner_ledger = []
        for prt_id in gen_led_data.keys():
            partner = {}
            currencies = []
            for cur_id in gen_led_data[prt_id].keys():
                currency = {}
                move_lines = []
                if not isinstance(cur_id, int):
                    partner.update({cur_id: gen_led_data[prt_id][cur_id]})
                else:
                    for ml_id in gen_led_data[prt_id][cur_id].keys():
                        if not isinstance(ml_id, int):
                            currency.update({ml_id: gen_led_data[prt_id][cur_id][ml_id]})
                        else:
                            move_lines += [gen_led_data[prt_id][cur_id][ml_id]]
                    move_lines = sorted(move_lines, key=lambda k: (k["date"]))
                    move_lines = self._recalculate_cumul_balance(
                        move_lines,
                        gen_led_data[prt_id][cur_id]["init_bal"]["balance"],
                        gen_led_data[prt_id][cur_id]["init_bal"]["bal_curr"],
                    )
                    currency.update({
                        "move_lines": move_lines,
                        "currency_id": currencies_data[cur_id]["currency_id"],
                    })
                    currencies += [currency]
            partner.update({
                "name": partners_data[prt_id]["name"],
                "currencies": currencies,
            })
            partner_ledger += [partner]
        return partner_ledger

    def _get_report_values(self, docids, data):
        wizard_id = data["wizard_id"]
        company = self.env["res.company"].browse(data["company_id"])
        company_id = data["company_id"]
        date_to = data["date_to"]
        date_from = data["date_from"]
        partner_ids = data["partner_ids"]
        account_ids = data["account_ids"]
        foreign_currency = data["foreign_currency"]
        only_posted_moves = data["only_posted_moves"]
        hide_exchange_diff = data["hide_exchange_diff"]
        gen_ld_data, partners_data, currency_ids = self._get_initial_balance_data(
            account_ids,
            partner_ids,
            company_id,
            date_from,
            foreign_currency,
            only_posted_moves,
            hide_exchange_diff,
        )

        (
            gen_ld_data,
            currencies_data,
            accounts_data,
            partners_data,
            journals_data,
        ) = self._get_period_ml_data(
            account_ids,
            partner_ids,
            company_id,
            foreign_currency,
            only_posted_moves,
            hide_exchange_diff,
            date_from,
            date_to,
            partners_data,
            gen_ld_data,
            currency_ids
        )
        partner_ledger = self._create_partner_ledger(
            gen_ld_data, partners_data, currencies_data)
        partner_ledger = sorted(partner_ledger, key=lambda k: k["name"])
        return {
            "doc_ids": [wizard_id],
            "doc_model": "partner.ledger.reports.wizard",
            "docs": self.env["partner.ledger.reports.wizard"].browse(wizard_id),
            "foreign_currency": data["foreign_currency"],
            "company_name": company.display_name,
            "company_currency_id": company.currency_id.id,
            "currency_name": company.currency_id.name,
            "date_from": data["date_from"],
            "date_to": data["date_to"],
            "only_posted_moves": data["only_posted_moves"],
            "partner_ledger": partner_ledger,
            "currencies_data": currencies_data,
            "partners_data": partners_data,
            "accounts_data": accounts_data,
            "journals_data": journals_data,
        }
