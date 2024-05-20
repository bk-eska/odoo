# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResCurrencyRateType(models.Model):
    _name = "res.currency.rate.type"
    _order = "name"
    _description = "Currency Rate Type"

    name = fields.Char(
        string="Name",
        required=True,
    )
