# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class IapAccount(models.Model):
    _inherit = "iap.account"

    @api.model
    def get_company_account(self, service_name, company_id, force_create=True):
        account = self.search([('service_name', '=', service_name),
                               ('company_ids', 'in', [company_id.id])], limit=1)
        if not account and force_create:
            account = self.create({
                'service_name': service_name,
                'company_ids':  [(6, 0, [company_id.id])],
            })
            self.env.cr.commit()
        return account
