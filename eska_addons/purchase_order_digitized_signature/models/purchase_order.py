# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    signature = fields.Image(string='Signature', help='Signature', copy=False, attachment=True, tracking=True)

    def purchase_order_unsign(self):
        self.signature = False

    @api.depends('signature')
    def _compute_is_signed(self):
        for order in self:
            order.is_signed = order.signature