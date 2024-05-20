# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, models


class PartnerBalanceXslx(models.AbstractModel):
    _name = "reports.account_partner_balance.report_partner_balance_xlsx"
    _description = "Partner Balance XLSX Report"
    _inherit = "reports.account_financial_report.abstract_report_xlsx"

    def _get_report_name(self, report, data=False):
        company_id = data.get("company_id", False)
        report_name = _("Partner Balance")
        if company_id:
            company = self.env["res.company"].browse(company_id)
            suffix = " - {} - {}".format(company.name, company.currency_id.name)
            report_name = report_name + suffix
        return report_name

    def _get_report_columns(self, report):
        res = {
            0: {"header": _("Partner"), "field": "partner_name", "width": 50},
            1: {
                "header": _("Debit"),
                "field": "total_debit",
                "field_final_balance": "debit",
                "type": "amount",
                "width": 25,
            },
            2: {
                "header": _("Credit"),
                "field": "total_credit",
                "field_final_balance": "credit",
                "type": "amount",
                "width": 25,
            },
        }
        return res

    def _get_report_filters(self, report):
        return [
            [_("Date at filter"), report.date_at.strftime("%d/%m/%Y")],
            [
                _("Target moves filter"),
                _("All posted entries")
                if report.target_move == "posted"
                else _("All entries"),
            ],
            [
                _("Account balance at 0 filter"),
                _("Hide") if report.hide_account_at_0 else _("Show"),
            ],
        ]

    def _get_col_count_filter_name(self):
        return 1

    def _get_col_count_filter_value(self):
        return 1

    def _get_col_count_final_balance_name(self):
        return 1

    def _get_col_pos_final_balance_label(self):
        return 0

    def _generate_report_content(self, workbook, report, data, report_data):
        res_data = self.env[
            "reports.account_partner_balance.partner_balance"
        ]._get_report_values(report, data)
        partners_data = res_data["partners_data"]
        total_debit = res_data['total_amount']["total_debit"] or False
        total_credit = res_data['total_amount']["total_credit"] or False

        self.write_array_header(report_data)
        type_object = ''
        line = {}
        for partner_id in partners_data.keys():
            line.update({
                'partner_name': partners_data[partner_id]['name'],
                'total_debit': partners_data[partner_id]["debit"] if partners_data[partner_id]["debit"] else False,
                'total_credit': partners_data[partner_id]["credit"] if partners_data[partner_id]["credit"] else False,
            })
            self.write_line_from_dict(line, report_data)
        self.write_ending_balance_from_dict(
            partners_data,
            type_object,
            total_debit,
            total_credit,
            report_data,
            account_id=False,
            partner_id=False
        )

    def write_ending_balance_from_dict(
        self,
        my_object,
        type_object,
        total_debit,
        total_credit,
        report_data,
        account_id=False,
        partner_id=False,
    ):
        my_object["debit"] = total_debit
        my_object["credit"] = total_credit
        label = _("Total balance")
        super(PartnerBalanceXslx, self).write_ending_balance_from_dict(
            my_object, type_object, label, report_data
        )
