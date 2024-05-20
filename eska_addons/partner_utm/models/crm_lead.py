# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        res = super()._prepare_customer_values(partner_name, is_company, parent_id)
        res.update({
            'source_id': self.source_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
        })
        return res
