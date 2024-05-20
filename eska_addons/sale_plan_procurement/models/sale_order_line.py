# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_uom_qty = fields.Float(
        default=0.0
    )

    requested_qty = fields.Float(
        string='Requested Qty',
        default=0.0,
        digits='Product Unit of Measure',
    )

    total_planned_qty = fields.Float(
        string='Total Planned Qty',
        digits='Product Unit of Measure',
        compute='_compute_total_planned_qty',
        compute_sudo=True,
        store=True,
    )

    procurement_summary = fields.Text(
        string='Procurement Summary',
        compute='_compute_procurement_summary',
        compute_sudo=True,
    )

    purchase_line_ids = fields.One2many(
        readonly=False,
    )

    stock_qty = fields.Float(
        string='Stock Quantity',
        related='product_id.qty_available',
    )

    stock_available_qty = fields.Float(
        string='Available Quantity',
        related='product_id.free_qty',
    )

    planned_stock_qty = fields.Float(
        string='Planned Stock Qty',
        digits='Product Unit of Measure',
    )

    unit_cost = fields.Float(
        string='Stock Unit Cost',
        related='product_id.standard_price'
    )

    @api.depends('purchase_line_ids.planned_qty', 'planned_stock_qty')
    def _compute_total_planned_qty(self):
        for line in self:
            line.total_planned_qty = sum(line.purchase_line_ids.mapped('planned_qty'))
            if line.planned_stock_qty > 0.0:
                line.total_planned_qty += line.planned_stock_qty

    @api.onchange('total_planned_qty')
    def _onchange_total_planned_qty(self):
        if self.total_planned_qty > 0.0:
            self.product_uom_qty = self.total_planned_qty

    def _get_product_cost(self, product_cost):
        if self._context.get('purchase_line'):
            pol = self.env['purchase.order.line'].browse(self._context.get('purchase_line'))
            fro_cur = pol.currency_id or pol.order_id.currency_id
        else:
            fro_cur = self.product_id.cost_currency_id
        to_cur = self.currency_id or self.order_id.currency_id
        if self.product_uom and self.product_uom != self.product_id.uom_id:
            product_cost = self.product_id.uom_id._compute_price(
                product_cost,
                self.product_uom,
            )
        return fro_cur._convert(
            from_amount=product_cost,
            to_currency=to_cur,
            company=self.company_id or self.env.company,
            date=fields.Date.today(),
            round=False,
        ) if to_cur and product_cost else product_cost

    @api.depends('purchase_line_ids.price_unit', 'total_planned_qty')
    def _compute_purchase_price(self):
        line_with_pol = self.filtered(lambda l: l.purchase_line_ids)
        for line in line_with_pol:
            line = line.with_company(line.company_id)
            total_price = 0.0
            for purchase_line in line.purchase_line_ids.filtered(lambda l: l.planned_qty > 0.0):
                purchase_price = line.with_context(purchase_line=purchase_line.id)._get_product_cost(purchase_line.price_unit)
                total_price += purchase_price * purchase_line.planned_qty
            if line.planned_stock_qty:
                purchase_price = line._get_product_cost(line.product_id.standard_price)
                total_price += purchase_price * line.planned_stock_qty

            if total_price > 0.0 and line.total_planned_qty > 0:
                purchase_price = total_price / line.total_planned_qty
                line.purchase_price = purchase_price
        return super(SaleOrderLine, self - line_with_pol)._compute_purchase_price()

    @api.depends('purchase_line_ids.planned_qty', 'planned_stock_qty')
    def _compute_procurement_summary(self):
        for line in self:
            summary = ''
            for purchase_line in line.purchase_line_ids.filtered(lambda l: l.planned_qty > 0.0):
                summary += f'{purchase_line.partner_id.name} : {purchase_line.planned_qty} {line.product_id.uom_id.name}' + ' \n'
            if line.planned_stock_qty:
                summary += f'Stock : {line.planned_stock_qty} {line.product_id.uom_id.name}'
            line.procurement_summary = summary
