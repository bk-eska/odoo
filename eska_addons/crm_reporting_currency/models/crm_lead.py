# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    company_currency = fields.Many2one(
        related='company_id.report_currency_id',
    )
