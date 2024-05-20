# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    report_currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='company_id.report_currency_id',
    )

    report_currency_unit_cost = fields.Monetary(
        string='Currency Unit Cost',
        compute='_compute_reporting_currency_value',
        store=True,
        help='Unit Cost In Report Currency',
    )

    report_currency_value = fields.Monetary(
        string='Total Currency Value',
        compute='_compute_reporting_currency_value',
        store=True,
        help='Total Value In Report Currency',
    )

    report_currency_remaining_value = fields.Monetary(
        string='Currency Remaining Value',
        compute='_compute_reporting_currency_value',
        store=True,
        help='Remaining Value In Report Currency',
    )

    @api.depends('company_id.report_currency_id', 'unit_cost', 'value', 'remaining_value')
    def _compute_reporting_currency_value(self):
        for rec in self:
            report_currency_unit_cost = rec.currency_id._convert(
                rec.unit_cost, rec.report_currency_id,
                rec.company_id, rec.create_date)
            report_currency_value = rec.currency_id._convert(
                rec.value, rec.report_currency_id,
                rec.company_id, rec.create_date)
            report_currency_remaining_value = rec.currency_id._convert(
                rec.remaining_value, rec.report_currency_id,
                rec.company_id, rec.create_date)
            rec.write({
                'report_currency_unit_cost': report_currency_unit_cost,
                'report_currency_value': report_currency_value,
                'report_currency_remaining_value': report_currency_remaining_value,
            })

