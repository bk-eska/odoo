# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools import float_is_zero


class ProductProduct(models.Model):
    _inherit = 'product.product'

    report_currency_value_svl = fields.Float(
        compute='_compute_report_currency_value_svl',
        compute_sudo=True
    )

    report_currency_avg_cost = fields.Monetary(
        string="Average Currency Cost",
        compute='_compute_report_currency_value_svl',
        compute_sudo=True,
        currency_field='report_currency_id',
    )

    report_currency_total_value = fields.Monetary(
        string="Total Currency Value",
        compute='_compute_report_currency_value_svl',
        compute_sudo=True,
        currency_field='report_currency_id',
    )

    report_currency_standard_price = fields.Float(
        string='Currency Cost',
        company_dependent=True,
        digits='Product Price',
    )

    @api.depends('stock_valuation_layer_ids')
    @api.depends_context('to_date', 'company')
    def _compute_report_currency_value_svl(self):
        company_id = self.env.company
        domain = [
            ('product_id', 'in', self.ids),
            ('company_id', '=', company_id.id),
        ]
        if self.env.context.get('to_date'):
            to_date = fields.Datetime.to_datetime(self.env.context['to_date'])
            domain.append(('create_date', '<=', to_date))
        groups = self.env['stock.valuation.layer']._read_group(domain, ['report_currency_value:sum', 'quantity:sum'], ['product_id'])
        products = self.browse()
        # Browse all products and compute products' quantities_dict in batch.
        self.env['product.product'].browse([group['product_id'][0] for group in groups]).sudo(False).mapped(
            'qty_available')
        for group in groups:
            product = self.browse(group['product_id'][0])
            report_currency_value_svl = company_id.report_currency_id.round(group['report_currency_value'])
            report_currency_avg_cost = report_currency_value_svl / group['quantity'] if group['quantity'] else 0
            product.report_currency_value_svl = report_currency_value_svl
            product.report_currency_avg_cost = report_currency_avg_cost
            product.report_currency_total_value = report_currency_avg_cost * product.sudo(False).qty_available
            products |= product
        remaining = (self - products)
        remaining.report_currency_value_svl = 0
        remaining.report_currency_avg_cost = 0
        remaining.report_currency_total_value = 0

    def _run_fifo(self, quantity, company):
        self.ensure_one()
        qty_to_take_on_candidates = quantity
        candidates = self.env['stock.valuation.layer'].sudo().search([
            ('product_id', '=', self.id),
            ('remaining_qty', '>', 0),
            ('company_id', '=', company.id),
        ])
        new_report_currency_standard_price = 0
        for candidate in candidates:
            qty_taken_on_candidate = min(qty_to_take_on_candidates, candidate.remaining_qty)
            candidate_unit_cost = candidate.report_currency_remaining_value / candidate.remaining_qty
            new_report_currency_standard_price = candidate_unit_cost
            qty_to_take_on_candidates -= qty_taken_on_candidate
            if float_is_zero(qty_to_take_on_candidates, precision_rounding=self.uom_id.rounding):
                if float_is_zero(candidate.remaining_qty, precision_rounding=self.uom_id.rounding):
                    next_candidates = candidates.filtered(lambda svl: svl.remaining_qty > 0)
                    new_report_currency_standard_price = next_candidates and next_candidates[0].report_currency_unit_cost or new_report_currency_standard_price
                break
        if new_report_currency_standard_price and self.cost_method == 'fifo':
            self.sudo().with_company(company.id).with_context(disable_auto_svl=True).report_currency_standard_price = new_report_currency_standard_price
        return super(ProductProduct, self)._run_fifo(quantity, company)

    def _run_fifo_vacuum(self, company=None):
        res = super(ProductProduct, self)._run_fifo_vacuum(company)
        product = self.with_company(company.id)
        if product.cost_method == 'average' and not float_is_zero(
                product.quantity_svl, precision_rounding=self.uom_id.rounding):
            product.sudo().with_context(disable_auto_svl=True).write(
                {'report_currency_standard_price': product.report_currency_value_svl / product.quantity_svl})
        return res

