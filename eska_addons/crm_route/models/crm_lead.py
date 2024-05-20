# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    partner_route_id = fields.Many2one(
        comodel_name='res.partner.route',
        compute='_compute_partner_route_id',
        store=True,
        readonly=False,
        string='Route',
    )

    @api.depends('partner_id')
    def _compute_partner_route_id(self):
        for rec in self:
            rec.partner_route_id = rec.partner_id.partner_route_id
