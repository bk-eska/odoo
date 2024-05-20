# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields
from odoo.addons.account.models.product import ACCOUNT_DOMAIN

class ProductCategory(models.Model):
    _inherit = "product.category"

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
