# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.reports'

    partner_classification_id = fields.Many2one(
        comodel_name='res.partner.classification',
        string='Partner Classification',
        readonly=True,
    )

    _depends = {
        'res.partner': ['classification_id'],
    }

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + \
               ", contact_partner.classification_id as partner_classification_id"

    def _from(self):
        return super()._from() + " LEFT JOIN res_partner contact_partner ON contact_partner.id = move.partner_id"
