# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='company_id.currency_id',
    )

    report_currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='company_id.report_currency_id',
    )

    costs_hour = fields.Float(
        compute='_compute_costs_hour',
    )

    report_currency_costs_hour = fields.Float(
        string='Currency Cost Per Hour',
        help='Specify reports currency cost of work center per hour.',
        default=0.0
    )

    @api.depends('currency_id', 'report_currency_costs_hour',
                 'company_id.report_currency_id')
    def _compute_costs_hour(self):
        for rec in self:
            rec.costs_hour = self.company_id.report_currency_id._convert(
                rec.report_currency_costs_hour, rec.currency_id,
                rec.company_id, fields.Datetime.now())
