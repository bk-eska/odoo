# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def _prepare_opportunity_quotation_context(self):
        res = super()._prepare_opportunity_quotation_context()
        if self.partner_assigned_id:
            res['default_partner_assigned_id'] = self.partner_assigned_id.id
        return res
