# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class AccountTaxOffice(models.Model):
    _description = "Tax Office"
    _name = 'account.tax.office'
    _order = "state_id, name"

    active = fields.Boolean(
        string='Active',
        default=True,
    )

    name = fields.Char(
        string='Name',
        required=True,
    )

    code = fields.Char(
        string='Code',
    )

    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='State',
        required=True
    )

