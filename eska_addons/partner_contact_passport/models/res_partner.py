# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    passport_ids = fields.One2many(
        comodel_name='res.partner.passport',
        inverse_name='partner_id',
        string='Passports',
    )
