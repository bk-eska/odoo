# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    final_customer_id = fields.Many2one(
        'res.partner',
        string='Final Customer',
        help='The final customer associated with this opportunity.'
    )

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.final_customer_id = self.partner_id
        else:
            self.final_customer_id = False

    def action_sale_quotations_new(self):
        res = super(CrmLead, self).action_sale_quotations_new()
        if self.final_customer_id:
            res['context']['default_final_customer_id'] = self.final_customer_id.id
        return res
