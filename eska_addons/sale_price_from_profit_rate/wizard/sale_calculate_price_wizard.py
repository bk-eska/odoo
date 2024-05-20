# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _, api
from odoo.exceptions import UserError


class SaleCalculatePriceWizard(models.TransientModel):
    _name = 'sale.calculate.price.wizard'
    _description = 'Sale Calculate Price Wizard'

    order_line = fields.Many2many(
        comodel_name='sale.order.line',
        string='Order Lines',
    )

    generate_type = fields.Selection(
        selection=[
            ('manual', 'Manual'),
            ('automatic', 'Automatic (Product + Category)')
        ],
        string='Mode',
        default='manual',
        required=True,
    )

    profit_rate = fields.Float(
        string="Profit Rate (%)",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'order_line' in fields_list and 'order_line' not in res:
            if self._context.get('active_model') == 'sale.order':
                order = self.env['sale.order'].browse(self._context.get('active_ids', []))
                lines = order.order_line
                profit_rate = order.partner_id.profit_rate
            elif self._context.get('active_model') == 'sale.order.line':
                lines = self.env['sale.order.line'].browse(self._context.get('active_ids', []))
                profit_rate = lines[0].order_id.partner_id.profit_rate
            res['order_line'] = [(6, 0, lines.ids)]
            res['profit_rate'] = profit_rate
        return res

    def action_calculate_price(self):
        if not any(state in self.order_line.mapped('state') for state in ['draft', 'sent']):
            raise UserError(_('You can only calculate the price of sale order lines with state in Draft or Sent'))
        for line in self.order_line.filtered(lambda l: l.purchase_price > 0.0):
            if self.generate_type == 'manual':
                profit_price = line.purchase_price * self.profit_rate / 100
            else:
                if line.product_id.profit_rate:
                    profit_price = line.purchase_price * line.product_id.profit_rate / 100
                elif line.product_id.categ_id.profit_rate:
                    profit_price = line.purchase_price * line.product_id.categ_id.profit_rate / 100
                else:
                    raise UserError(_('Product %s does not have target profit rate!' % line.product_id.name))
            line.price_unit = line.purchase_price + profit_price
