# Copyright 2023 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class LoyaltyReward(models.Model):
    _inherit = 'loyalty.reward'

    deposit = fields.Boolean(
        string="Deposit",
    )
