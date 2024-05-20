# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_add_sale_line(self):
        self.ensure_one()
        return {
            'name': _('Add Sale Line'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'invoice.add.sale.line.wizard',
            'target': 'new',
            'context': {
                'default_partner_id': self.partner_id.id,
            },
        }