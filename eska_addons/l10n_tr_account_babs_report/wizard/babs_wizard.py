# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class BABSWizard(models.TransientModel):
    _name = 'babs.reports.wizard'
    _description = 'Print BA-BS Report by Period'

    date_range_id = fields.Many2one(
        comodel_name='date.range',
        string='Date Range',
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

    declaration_type = fields.Selection(
        selection=[
            ('sale', 'Sale Declaration'),
            ('purchase', 'Purchase Declaration'),
            ('sale_purchase', 'Sale and Purchase Declaration')
        ],
        string='Declaration',
        default='sale',
        required=True,
    )

    threshold = fields.Float(
        string='Theshold',
        required=True,
        default=5000.00,
        digits='Product Price',
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    @api.onchange("date_range_id")
    def onchange_date_range_id(self):
        if self.date_range_id:
            self.date_from = self.date_range_id.date_start
            self.date_to = self.date_range_id.date_end

    def button_export_pdf(self):
        self.ensure_one()
        report_type = "qweb-pdf"
        return self._export(report_type)

    def button_export_xlsx(self):
        self.ensure_one()
        report_type = "xlsx"
        return self._export(report_type)

    def button_export_xml_txt(self):
        self.ensure_one()
        report_type = "qweb-xml"
        return self._export(report_type)

    def _print_report(self, report_type):
        self.ensure_one()
        data = self._prepare_report_babs()
        if report_type == "xlsx":
            report_name = "l10n_tr_account_babs_report.report_babs_xlsx"
        elif report_type == "qweb-xml":
            report_name = "l10n_tr_account_babs_report.report_babs_xml"
        else:
            report_name = "l10n_tr_account_babs_report.report_babs"
        return (
            self.env["ir.actions.reports"].search(
                [("report_name", "=", report_name),
                 ("report_type", "=", report_type)],
                limit=1,
            ).report_action(self, data=data)
        )

    def _prepare_report_babs(self):
        self.ensure_one()
        return {
            "wizard_id": self.id,
            "company_id": self.company_id.id,
            "date_range_id": self.date_range_id.id,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "threshold": self.threshold,
            "declaration_type": self.declaration_type,
            "only_posted_moves": self.target_move == "posted",
        }

    def _export(self, report_type):
        return self._print_report(report_type)
