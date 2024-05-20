# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    mo_id = fields.Many2one(
        comodel_name='mrp.production',
        string='Manufacturing Order',
        readonly=True,
        copy=False
    )

    def unlink(self):
        self = self.sudo()
        for line in self:
            if line.mo_id and line.mo_id.state != 'cancel':
                raise ValidationError(_("You are trying to delete one or more products with active manufacturing orders"))
        return super().unlink()
