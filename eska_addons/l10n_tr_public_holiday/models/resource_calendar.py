# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    auto_update = fields.Boolean(
        string='Auto Update Holidays',
        default=True,
    )
