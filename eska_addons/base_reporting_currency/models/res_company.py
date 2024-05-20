# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model
    def _get_default_reporting_currency(self):
        return self.env['res.currency'].search(
            [('name', '=', 'USD')], limit=1)

    report_currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Reporting Currency',
        required=True,
        default=_get_default_reporting_currency
    )
