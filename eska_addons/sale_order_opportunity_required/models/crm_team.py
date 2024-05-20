# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, api, fields, exceptions


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    opportunity_required = fields.Boolean(
        string='Opportunity Required',
        default=True,
    )
