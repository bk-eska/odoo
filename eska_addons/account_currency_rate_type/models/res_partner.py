# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sale_currency_rate_type_id = fields.Many2one(
        comodel_name='res.currency.rate.type',
        string='Sale Currency Rate Type',
        help="Default currency rate type for sales",
        company_dependent=True,
    )

    purchase_currency_rate_type_id = fields.Many2one(
        comodel_name='res.currency.rate.type',
        string='Purchase Currency Rate Type',
        help="Default currency rate type for purchase",
        company_dependent=True,
    )
