# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import operator
from datetime import date, datetime

from odoo import api, models
from odoo.tools import float_is_zero


class PartnerBalanceReport(models.AbstractModel):
    _name = "reports.account_partner_balance.partner_balance"
    _description = "Partner Balance Report"
    _inherit = "reports.account_financial_report.abstract_report"

    def _get_account_partial_reconciled(self, company_id, date_at_object):
        domain = [("max_date", ">", date_at_object), ("company_id", "=", company_id)]
        fields = ["debit_move_id", "credit_move_id", "amount"]
        accounts_partial_reconcile = self.env["account.partial.reconcile"].search_read(
            domain=domain, fields=fields
        )
        debit_amount = {}
        credit_amount = {}
        for account_partial_reconcile_data in accounts_partial_reconcile:
            debit_move_id = account_partial_reconcile_data["debit_move_id"][0]
            credit_move_id = account_partial_reconcile_data["credit_move_id"][0]
            if debit_move_id not in debit_amount.keys():
                debit_amount[debit_move_id] = 0.0
            debit_amount[debit_move_id] += account_partial_reconcile_data["amount"]
            if credit_move_id not in credit_amount.keys():
                credit_amount[credit_move_id] = 0.0
            credit_amount[credit_move_id] += account_partial_reconcile_data["amount"]
            account_partial_reconcile_data.update(
                {"debit_move_id": debit_move_id, "credit_move_id": credit_move_id}
            )
        return accounts_partial_reconcile, debit_amount, credit_amount

    def _get_data(
        self,
        account_ids,
        partner_ids,
        date_at_object,
        only_posted_moves,
        company_id,
        date_from,
    ):
        domain = self._get_move_lines_domain_not_reconciled(
            company_id, account_ids, partner_ids, only_posted_moves, date_from
        )
        ml_fields = [
            "id",
            "date",
            "partner_id",
            "amount_residual",
            "debit",
            "credit",
            "reconciled",
            "currency_id",
        ]
        move_lines = self.env["account.move.line"].search_read(
            domain=domain, fields=ml_fields
        )
        partners_ids = set()
        partners_data = {}
        if date_at_object < date.today():
            (
                acc_partial_rec,
                debit_amount,
                credit_amount,
            ) = self._get_account_partial_reconciled(company_id, date_at_object)
            if acc_partial_rec:
                ml_ids = list(map(operator.itemgetter("id"), move_lines))
                debit_ids = list(
                    map(operator.itemgetter("debit_move_id"), acc_partial_rec)
                )
                credit_ids = list(
                    map(operator.itemgetter("credit_move_id"), acc_partial_rec)
                )
                move_lines = self._recalculate_move_lines(
                    move_lines,
                    debit_ids,
                    credit_ids,
                    debit_amount,
                    credit_amount,
                    ml_ids,
                    account_ids,
                    company_id,
                    partner_ids,
                    only_posted_moves,
                )
        move_lines = [
            move_line
            for move_line in move_lines
            if move_line["date"] <= date_at_object
               and not float_is_zero(move_line["amount_residual"], precision_digits=2)
        ]

        partner_balance_move_lines_data = {}
        for move_line in move_lines:
            if move_line["partner_id"]:
                prt_id = move_line["partner_id"][0]
                prt_name = move_line["partner_id"][1]
            else:
                prt_id = 0
                prt_name = "Missing Partner"
            if prt_id not in partners_ids:
                partners_data.update({prt_id: {"id": prt_id, "name": prt_name}})
                partners_ids.add(prt_id)

            move_line.update(
                {
                    "partner_id": prt_id,
                    "partner_name": prt_name,
                    "currency_id": move_line["currency_id"][0]
                    if move_line["currency_id"]
                    else False,
                    "currency_name": move_line["currency_id"][1]
                    if move_line["currency_id"]
                    else False,
                }
            )
            if prt_id not in partner_balance_move_lines_data.keys():
                partner_balance_move_lines_data[prt_id] = [move_line]
            else:
                partner_balance_move_lines_data[prt_id].append(move_line)

        return (
            move_lines,
            partners_data,
            partner_balance_move_lines_data,
        )

    @api.model
    def _calculate_amounts(self, partner_balance_move_lines_data, partners_data):
        total_amount = {}
        total_amount['total_debit'] = 0.0
        total_amount['total_credit'] = 0.0
        for partner_id in partner_balance_move_lines_data.keys():
            total_amount[partner_id] = {}
            residual = 0.0
            for move_line in partner_balance_move_lines_data[partner_id]:
                residual += move_line["amount_residual"]
            if self._context.get('hide') and float_is_zero(residual, precision_digits=2):
                partners_data.pop(partner_id)
            else:
                if residual > 0.0:
                    total_amount['total_credit'] += residual
                    partners_data[partner_id]['credit'] = residual
                    partners_data[partner_id]['debit'] = ''
                elif residual < 0.0:
                    total_amount['total_debit'] += residual
                    partners_data[partner_id]['debit'] = residual
                    partners_data[partner_id]['credit'] = ''
                else:
                    partners_data[partner_id]['debit'] = ''
                    partners_data[partner_id]['credit'] = ''
        return total_amount

    @api.model
    def _order_partner_balance_by_date(
            self, partners_data
    ):
        new_partner_data = {}
        for prt_id in sorted(
                partners_data,
                key=lambda i: partners_data[i]["name"],
        ):
            new_partner_data[prt_id] = {}
            for key, value in partners_data[prt_id].items():
                new_partner_data[prt_id][key] = value
        return new_partner_data

    def _get_report_values(self, docids, data):
        wizard_id = data["wizard_id"]
        company = self.env["res.company"].browse(data["company_id"])
        company_id = data["company_id"]
        account_ids = data["account_ids"]
        partner_ids = data["partner_ids"]
        date_at = data["date_at"]
        date_at_object = datetime.strptime(date_at, "%Y-%m-%d").date()
        date_from = data["date_from"]
        only_posted_moves = data["only_posted_moves"]

        (
            move_lines_data,
            partners_data,
            partner_balance_move_lines_data,
        ) = self._get_data(
            account_ids,
            partner_ids,
            date_at_object,
            only_posted_moves,
            company_id,
            date_from,
        )

        total_amount = self.with_context(hide=data["hide_account_at_0"]).\
            _calculate_amounts(partner_balance_move_lines_data, partners_data)
        partners_data = self._order_partner_balance_by_date(partners_data)
        return {
            "doc_ids": [wizard_id],
            "doc_model": "partner.balance.reports.wizard",
            "docs": self.env["partner.balance.reports.wizard"].browse(wizard_id),
            "company_name": company.display_name,
            "currency_name": company.currency_id.name,
            "date_at": date_at_object.strftime("%d/%m/%Y"),
            "hide_account_at_0": data["hide_account_at_0"],
            "target_move": data["target_move"],
            "partners_data": partners_data,
            "total_amount": total_amount,
        }
