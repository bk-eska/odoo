# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class LeadGeneratorWizard(models.TransientModel):
    _name = 'invoice.add.sale.line.wizard'
    _description = 'Invoice Add Sale Line'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
    )

    sale_line_ids = fields.Many2many(
        comodel_name='sale.order.line',
        string='Sale Lines',
        domain="[('order_partner_id', '=', partner_id),"
               "('invoice_status', 'not in', ['no', 'invoiced'])]",
        required=True,
    )

    def action_add_sale_line_and_new(self):
        self.action_add_sale_line()
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

    def action_add_sale_line(self):
        invoice = self.env['account.move'].browse(self._context.get('active_id'))
        for sale_line in self.sale_line_ids:
            invoice_line_vals = sale_line._prepare_invoice_line()
            invoice_line_vals['quantity'] = sale_line.qty_to_invoice
            invoice_line_vals['move_id'] = invoice.id
            self.env['account.move.line'].create(invoice_line_vals)
