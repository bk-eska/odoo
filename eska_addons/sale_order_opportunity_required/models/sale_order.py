# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    opportunity_required = fields.Boolean(
        related='team_id.opportunity_required',
        string='Opportunity Required',
    )
