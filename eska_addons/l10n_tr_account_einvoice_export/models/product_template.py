# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    l10n_tr_einvoice_shipment_cost = fields.Boolean(
        string="Shipping Cost",
        help="An line with this product will be hidden in export invoices."
    )

    l10n_tr_einvoice_insurance_cost = fields.Boolean(
        string="Insurance Cost",
        help="An line with this product will be hidden in export invoices."
    )
