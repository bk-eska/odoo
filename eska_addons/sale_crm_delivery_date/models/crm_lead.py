# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    commitment_date = fields.Datetime(
        string="Delivery Date",
        help="Expected date you can promise to the customer",
    )

    def _prepare_opportunity_quotation_context(self):
        res = super()._prepare_opportunity_quotation_context()
        if self.commitment_date:
            res['default_commitment_date'] = self.commitment_date
        return res
