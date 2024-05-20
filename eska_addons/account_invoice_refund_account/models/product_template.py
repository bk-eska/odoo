# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.account.models.product import ACCOUNT_DOMAIN

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    property_account_in_refund_id = fields.Many2one(
        comodel_name='account.account',
        string='In Refund Account',
        domain=ACCOUNT_DOMAIN,
        company_dependent=True,
    )

    property_account_out_refund_id = fields.Many2one(
        comodel_name='account.account',
        string='Out Refund Account',
        domain=ACCOUNT_DOMAIN,
        company_dependent=True,
    )

    def _get_product_accounts(self):
        res = super(ProductTemplate, self)._get_product_accounts()
        if ('move_type' in self._context and
                self._context.get('move_type') in ['out_refund', 'in_refund']):
            refund_out = self.property_account_out_refund_id or \
                         self.categ_id.property_account_out_refund_id
            if refund_out:
                res['income'] = refund_out
            refund_in = self.property_account_in_refund_id or \
                        self.categ_id.property_account_in_refund_id
            if refund_in:
                res['expense'] = refund_in
        return res
