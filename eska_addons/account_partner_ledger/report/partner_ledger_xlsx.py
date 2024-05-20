# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, models


class PartnerLedgerXslx(models.AbstractModel):
    _name = "reports.account_partner_ledger.report_partner_ledger_xlsx"
    _description = "Partner Ledger XLSX Report"
    _inherit = "reports.account_financial_report.abstract_report_xlsx"

    def _get_report_name(self, report, data=False):
        report_name = _("Partner Ledger")
        if report.company_id:
            suffix = " - {}".format(report.company_id.name)
            report_name = report_name + suffix
        return report_name

    def _get_report_columns(self, report):
        res = [
            {"header": _("Date"), "field": "date", "width": 11},
            {"header": _("Maturity"), "field": "date_maturity", "width": 11},
            {"header": _("Entry"), "field": "entry", "width": 18},
            {"header": _("Journal"), "field": "journal", "width": 8},
            {"header": _("Account"), "field": "account", "width": 9},
            {"header": _("Ref - Label"), "field": "ref", "width": 40},
            {
                "header": _("Debit"),
                "field": "debit",
                "field_initial_balance": "initial_debit",
                "field_final_balance": "final_debit",
                "type": "amount",
                "width": 14,
            },
            {
                "header": _("Credit"),
                "field": "credit",
                "field_initial_balance": "initial_credit",
                "field_final_balance": "final_credit",
                "type": "amount",
                "width": 14,
            },
            {
                "header": _("Cumul. Bal."),
                "field": "balance",
                "field_initial_balance": "initial_balance",
                "field_final_balance": "final_balance",
                "type": "amount",
                "width": 14,
            },
        ]
        if report.foreign_currency:
            res += [
                {
                    "header": _("Cur. Rate"),
                    "field": "currency_rate",
                    "type": "currency_rate",
                    "width": 14,
                },
                {
                    "header": _("Amount cur."),
                    "field": "amount_currency",
                    "type": "amount_currency",
                    "width": 14,
                },
                {
                    "header": _("Balance cur."),
                    "field": "bal_curr",
                    "field_initial_balance": "initial_bal_curr",
                    "field_final_balance": "final_bal_curr",
                    "type": "amount_currency",
                    "width": 14,
                }
            ]
        res_as_dict = {}
        for i, column in enumerate(res):
            res_as_dict[i] = column
        return res_as_dict

    def _get_report_filters(self, report):
        return [
            [
                ("Date range filter"),
                ("From: %(date_from)s To: %(date_to)s")
                % ({"date_from": report.date_from, "date_to": report.date_to}),
            ],
            [
                _("Target moves filter"),
                _("All posted entries")
                if report.target_move == "all"
                else _("All entries"),
            ],
            [
                _("Show foreign currency"),
                _("Yes") if report.foreign_currency else _("No"),
            ],
        ]

    def _get_col_count_filter_name(self):
        return 2

    def _get_col_count_filter_value(self):
        return 2

    def _get_col_pos_initial_balance_label(self):
        return 5

    def _get_col_count_final_balance_name(self):
        return 5

    def _get_col_pos_final_balance_label(self):
        return 5

    # flake8: noqa: C901
    def _generate_report_content(self, workbook, report, data, report_data):
        res_data = self.env[
            "reports.account_partner_ledger.partner_ledger"
        ]._get_report_values(report, data)
        partner_ledger = res_data["partner_ledger"]
        accounts_data = res_data["accounts_data"]
        journals_data = res_data["journals_data"]
        foreign_currency = res_data["foreign_currency"]
        # For each currency
        for partner in partner_ledger:
            for currency in partner['currencies']:
                # Write account title
                self.write_array_title(
                    partner["name"] + (' - ' + currency['name'])
                    if foreign_currency else '',
                    report_data
                )
                # Display array header for move lines
                self.write_array_header(report_data)
                currency.update(
                    {
                        "initial_debit": currency["init_bal"]["debit"],
                        "initial_credit": currency["init_bal"]["credit"],
                        "initial_balance": currency["init_bal"]["balance"],
                        "currency_id": currency["currency_id"],
                    }
                )
                if foreign_currency:
                    currency.update(
                        {"initial_bal_curr": currency["init_bal"]["bal_curr"]}
                    )
                self.write_initial_balance_from_dict(currency,
                                                     _("Initial balance"),
                                                     report_data)

                # Display account move lines
                for line in currency["move_lines"]:
                    line.update(
                        {
                            "account": accounts_data[line["account_id"]]["code"],
                            "journal": journals_data[line["journal_id"]]["code"],
                        }
                    )
                    if line["currency_id"]:
                        line.update(
                            {
                                "currency_name": line["currency_id"][1],
                                "currency_id": line["currency_id"][0],
                            }
                        )
                    self.write_line_from_dict(line, report_data)

                    # Display ending balance line for partner
                    currency.update(
                        {
                            "final_debit": currency["fin_bal"]["debit"],
                            "final_credit": currency["fin_bal"]["credit"],
                            "final_balance": currency["fin_bal"]["balance"],
                        }
                    )
                    if foreign_currency:
                        currency.update(
                            {"final_bal_curr": currency["fin_bal"]["bal_curr"]}
                        )
                self.write_ending_balance_from_dict(currency,
                                                    currency["name"],
                                                    _("Ending balance"),
                                                    report_data)
                # line break
                report_data["row_pos"] += 1

            # 2 lines break
            report_data["row_pos"] += 2

    def write_line_from_dict(self, line_dict, report_data):
        """Write a line on current line"""
        for col_pos, column in report_data["columns"].items():
            value = line_dict.get(column["field"], False)
            cell_type = column.get("type", "string")
            # We will use a special cell type according to the currency of
            # record and the company's currency:
            # - If the currency is the same as the company's currency, we will leave
            # the value empty.
            # - If the currency is different from the company's currency, we will
            # show the value.
            if cell_type == "amount_different_company_currency":
                if line_dict.get("currency_id") and line_dict.get(
                    "company_currency_id"
                ):
                    if line_dict["currency_id"] == line_dict["company_currency_id"]:
                        value = ""
                        cell_type = "string"
                    else:
                        cell_type = "amount_currency"
            # All conditions according to cell type.
            if cell_type == "string":
                if line_dict.get("type", "") == "group_type":
                    report_data["sheet"].write_string(
                        report_data["row_pos"],
                        col_pos,
                        value or "",
                        report_data["formats"]["format_bold"],
                    )
                else:
                    if (
                        not isinstance(value, str)
                        and not isinstance(value, bool)
                        and not isinstance(value, int)
                    ):
                        value = value and value.strftime("%d/%m/%Y")
                    report_data["sheet"].write_string(
                        report_data["row_pos"], col_pos, value or ""
                    )
            elif cell_type == "amount":
                if (
                    line_dict.get("account_group_id", False)
                    and line_dict["account_group_id"]
                ):
                    cell_format = report_data["formats"]["format_amount_bold"]
                else:
                    cell_format = report_data["formats"]["format_amount"]
                report_data["sheet"].write_number(
                    report_data["row_pos"], col_pos, float(value), cell_format
                )
            elif cell_type == "amount_currency":
                if line_dict.get("currency_name", False):
                    format_amt = self._get_currency_amt_format_dict(
                        line_dict, report_data
                    )
                    report_data["sheet"].write_number(
                        report_data["row_pos"], col_pos, float(value), format_amt
                    )
            elif cell_type == "currency_name":
                report_data["sheet"].write_string(
                    report_data["row_pos"],
                    col_pos,
                    value or "",
                    report_data["formats"]["format_right"],
                )
            elif cell_type == "currency_rate":
                if line_dict.get("currency_id", False):
                    format_rate = report_data["workbook"].add_format()
                    format_rate.set_num_format("#,##0.0000")
                    report_data["sheet"].write_number(
                        report_data["row_pos"], col_pos, float(value), format_rate
                    )
        report_data["row_pos"] += 1
