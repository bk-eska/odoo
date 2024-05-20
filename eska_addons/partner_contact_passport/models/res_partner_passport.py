# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerPassport(models.Model):
    _name = "res.partner.passport"
    _description = "Partner Passport"
    _order =  "expire_date DESC"

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
    )

    name = fields.Char(
        string="Passport No",
        required=True,
    )

    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country ID',
        required=True,
    )

    expire_date = fields.Date(
        string="Expiration Date",
        help="Expiration date of the passport.",
        required=True,
    )
