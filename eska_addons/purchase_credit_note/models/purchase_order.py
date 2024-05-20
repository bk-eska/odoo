# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.tools import groupby, float_is_zero


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_return = fields.Boolean(
        string='Is Return',
    )

    def _prepare_invoice(self):
        if self.is_return:
            self = self.with_context(default_move_type='out_refund')
        return super(PurchaseOrder, self)._prepare_invoice()
