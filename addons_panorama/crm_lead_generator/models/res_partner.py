# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    schedule_duration = fields.Integer(
        string='Schedule Duration',
        default=14,
    )

    date_last_opportunity = fields.Date(
        string='Last Opportunity Date',
        compute='_compute_last_opportunity_date',
        store=True,
    )

    @api.constrains("schedule_duration")
    def check_schedule_duration(self):
        for record in self:
            if record.schedule_duration <= 0:
                raise ValidationError(
                    _("Duration must be greater than 0")
                )

    @api.depends('opportunity_ids')
    def _compute_last_opportunity_date(self):
        for rec in self:
            rec.date_last_opportunity = self.env['crm.lead'].search([
                ('partner_id', '=', rec.id),
                ('date_deadline', '!=', False),
            ], order='date_deadline desc', limit=1).date_deadline
