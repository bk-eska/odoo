# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields
from dateutil.relativedelta import relativedelta


class StockLedgerReportWizard(models.TransientModel):
    _name = 'stock.ledger.reports.wizard'
    _description = 'Stock Ledger Report Wizard'

    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Location',
        domain="[('usage', '=', 'internal')]",
    )
    start_date = fields.Date(
        string='Start Date',
        default=lambda self: fields.Date.today() + relativedelta(month=1, day=1),
        required=True,
    )
    end_date = fields.Date(
        string='Start Date',
        default=lambda self: fields.Date.today(),
        required=True,
    )
    show_price = fields.Boolean(
        string='Show Price',
    )

    product_ids = fields.Many2many(
        'product.product',
        string='Products',
    )

    def action_export_stock_report(self):
        data = {
            'location_id': self.location_id.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'show_price': self.show_price,
            'product_ids': self.product_ids.ids,
        }
        return self.env.ref('stock_ledger_report.stock_ledger_report_xlsx').report_action(self, data=data)
