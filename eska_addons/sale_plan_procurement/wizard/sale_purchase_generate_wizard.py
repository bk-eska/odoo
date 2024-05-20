# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _
from odoo.exceptions import UserError


class SalePurchaseGenerateWizard(models.TransientModel):
    _name = 'sale.purchase.generate.wizard'
    _description = 'Sale Purchase Generate Wizard'

    def _order_line_ids_domain(self):
        return [('order_id', '=', self._context.get("active_ids", []))]

    generate_type = fields.Selection(
        selection=[
            ('manual', 'Manual'),
            ('automatic', 'Automatic (Product + Category)')
        ],
        string='Mode',
        default='manual',
        required=True,
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Vendor',
    )

    def create_po_order(self, vendor, sale_line):
        po_line = self.env['purchase.order.line'].search([
            ('sale_line_id.order_id', '=', sale_line.order_id.id),
            ('order_id.partner_id', '=', vendor.id),
            ('state', '=', 'draft'),
        ])
        if po_line.product_id == sale_line.product_id:
            return
        fiscal_position = sale_line.order_id.fiscal_position_id
        taxes = fiscal_position.map_tax(sale_line.product_id.supplier_taxes_id)
        if taxes:
            taxes = taxes.filtered(lambda t: t.company_id.id == self.env.company.id)
        price_unit = 0.0
        requisition_line = self.env['purchase.requisition.line'].search([
            ('requisition_id.vendor_id', '=', vendor.id),
            ('requisition_id.date_end', '>=', fields.Datetime.now()),
            ('product_id', '=', sale_line.product_id.id),
            ('requisition_id.state', 'not in', ['draft', 'done', 'cancel']),
        ], order='id desc', limit=1)
        if requisition_line:
            price_unit = requisition_line.requisition_id.currency_id._convert(
                requisition_line.price_unit,
                sale_line.order_id.currency_id,
                sale_line.order_id.company_id,
                fields.Date.today(),
            )
            price_unit = self.env['account.tax']._fix_tax_included_price_company(
                sale_line.product_id.uom_id._compute_price(
                    price_unit,
                    sale_line.product_id.uom_id
                ),
                sale_line.product_id.supplier_taxes_id,
                taxes,
                self.env.company,
            )

        vals = {
            'product_id': sale_line.product_id.id,
            'name': sale_line.name,
            'product_qty': sale_line.requested_qty,
            'planned_qty': 0.0,
            'product_uom': sale_line.product_id.uom_id.id,
            'price_unit': price_unit,
            'sale_line_id': sale_line.id,
        }
        if po_line and po_line.product_id != sale_line.product_id:
            vals['order_id'] = po_line.order_id.id
            self.env['purchase.order.line'].create(vals)
        else:
            self.env['purchase.order'].create({
                'partner_id': vendor.id,
                'origin': sale_line.order_id.name,
                'order_line': [(0, 0, vals)],
            })

    def generate_purchase(self):
        line_ids = self.env["sale.order.line"].browse(self._context.get("active_ids", []))
        for line in line_ids:
            if self.generate_type == 'manual':
                self.create_po_order(self.partner_id, line)
            else:
                if line.product_id.vendor_ids:
                    for vendor in line.product_id.vendor_ids:
                        self.create_po_order(vendor, line)
                elif line.product_id.categ_id.vendor_ids:
                    for vendor in line.product_id.categ_id.vendor_ids:
                        self.create_po_order(vendor, line)
                else:
                    raise UserError(
                        _('Product %s does not have any vendor on it and on category of it' % line.product_id.name))
