# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCurrencyRate(models.Model):
    _inherit = "res.currency.rate"

    rate = fields.Float(
        digits='Currency Rate',
    )

    company_rate = fields.Float(
        digits='Currency Rate',
    )

    inverse_company_rate = fields.Float(
        digits='Currency Inverse Rate',
    )
