# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class AccountVatReportWizard(models.TransientModel):
    _name = 'account.vat.reports.wizard'
    _description = 'Account VAT Return Report Wizard'

    date_range_id = fields.Many2one(
        comodel_name='date.range',
        string='Date Range',
        required=True,
    )

    def generate_report(self):
        data = {
            'date_range_id': self.date_range_id.id,
        }
        return self.env.ref('l10n_tr_account_vat_return_report.vat_report_xlsx').report_action(self, data=data)
