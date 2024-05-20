# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta, datetime
from odoo import models, fields


class LeadGeneratorWizard(models.TransientModel):
    _name = 'lead.generator.wizard'

    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Customers',
    )

    start_date = fields.Date(
        string='Start Date',
        required=True,
    )

    final_date = fields.Date(
        string='Final Date',
        required=True,
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        domain=[('share', '=', False)],
    )

    stage_id = fields.Many2one(
        comodel_name='crm.stage',
        string='Stage',
    )

    recreate = fields.Boolean(
        string='Recreate',
        help='If checked, the newer opportunities will be deleted and created again',
    )

    mail_activity_type_id = fields.Many2one(
        comodel_name='mail.activity.type',
        string='Activity Type'
    )

    def action_generate_lead(self):
        for partner in self.partner_ids:
            partner_lead = self.env['crm.lead'].search([
                ('partner_id', '=', partner.id),
                ('type', '=', 'opportunity'),
            ], order='date_deadline desc', limit=1)
            if self.start_date:
                date = self.start_date
            elif not self.start_date and partner_lead and partner_lead.date_deadline \
                    and partner_lead.date_deadline > fields.Date.today():
                date = partner_lead.date_deadline
            else:
                date = fields.Date.today()
            if self.recreate:
                newer_leads = self.env['crm.lead'].search([
                    ('partner_id', '=', partner.id),
                    ('type', '=', 'opportunity'),
                    ('date_deadline', '>=', date),
                ])
                newer_leads.unlink()

            if partner.schedule_duration <= 0:
                duration = timedelta(days=14)
            else:
                duration = timedelta(days=partner.schedule_duration)

            invoices = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
                ('move_type', '=', 'out_invoice'),
            ], order='invoice_date desc', limit=3).mapped('amount_total')
            revenue = 0
            if invoices:
                revenue = sum(invoices)/len(invoices)
            lang = self.env.context.get('lang') or self.env.user.company_id.partner_id.lang or 'en_US'

            while self.final_date >= date:
                user = self.user_id if self.user_id else partner.user_id
                lead = self.env['crm.lead'].create({
                    'type': 'opportunity',
                    'user_id': user.id,
                    'name': 'Sales for ' + partner.name + ' ' + date.strftime(self.env['res.lang']._lang_get(lang).date_format),
                    'partner_id': partner.id,
                    'expected_revenue': revenue,
                    'probability': 75.0,
                    'date_deadline': date,
                })
                if self.stage_id:
                    lead.stage_id = self.stage_id
                self.env['mail.activity'].sudo().create({
                    'res_id': lead.id,
                    'date_deadline': lead.date_deadline,
                    'activity_type_id': self.mail_activity_type_id.id,
                    'summary': 'Sales for ' + partner.name + ' ' + date.strftime(self.env['res.lang']._lang_get(lang).date_format),
                    'user_id': lead.user_id.id,
                    'res_model_id': self.env.ref('crm.model_crm_lead').id,
                })
                date += duration
