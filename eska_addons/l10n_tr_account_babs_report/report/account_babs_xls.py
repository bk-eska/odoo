# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, models


class PartnerBalanceXslx(models.AbstractModel):
    _name = "reports.l10n_tr_account_babs_report.report_babs_xlsx"
    _description = "BA BS XLSX Report"
    _inherit = 'reports.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        res_data = self.env[
            "reports.l10n_tr_account_babs_report.report_babs"
        ]._get_report_values(docids=False, data=data)
        only_posted_moves = res_data["only_posted_moves"]
        entries = _("All posted entries") if only_posted_moves else _("All entries")
        company_name = res_data["company_name"]
        currency_name = res_data["currency_name"]
        declaration_type = res_data['declaration_type']
        reports = res_data["reports"]
        style = workbook.add_format({'font_size': 12})
        style_bold = workbook.add_format({'font_size': 12, 'bold': True})

        for report in reports:
            title = f"{company_name} - {report['title']} - {entries} - {currency_name}"
            sheet = workbook.add_worksheet(report['title_short'])
            sheet.write(0, 0, title, style_bold)
            col = 0
            row = 1
            headers = [
                "Sıra No",
                "İş Ortağı",
                "Ülke",
                "Vergi No",
                "Ulusal Kimlik",
                "Adet",
                "Vergisiz Tutar",
            ]
            for header in headers:
                sheet.write(row, col, header, style_bold)
                sheet.set_column(col, col, 20)
                col += 1

            row += 1
            rows = []
            i = 1
            for partner in report['partners']:
                rows.append((
                    i,
                    partner.get('partner_name', ''),
                    partner.get('country_name', ''),
                    partner.get('tax_id', ''),
                    partner.get('national_id', ''),
                    partner.get('count', 0),
                    partner.get('amount_untaxed', 0.0),
                ))
                i += 1
            for partner_row in rows:
                col = 0
                for partner_data in partner_row:
                    sheet.write(row, col, partner_data, style)
                    col += 1
                row += 1



