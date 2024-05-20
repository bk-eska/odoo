# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    contract_id = fields.Many2one(
        comodel_name='contract.contract',
        string='Contract',
    )
