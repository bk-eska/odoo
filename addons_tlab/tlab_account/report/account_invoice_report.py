# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.reports'

    country_group_id = fields.Many2one(
        comodel_name='res.country.group',
        string='Country Group',
    )

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + ", country.country_group_id as country_group_id"

    def _from(self):
        return super()._from() + \
            '''LEFT JOIN res_country country ON country.id = commercial_partner.country_id '''
