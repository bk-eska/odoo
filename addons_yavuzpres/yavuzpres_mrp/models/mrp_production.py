# Copyright 2023 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    qty_produced = fields.Float(
        string='Produced Quantity',
        store=True,
    )

    qty_remaining = fields.Float(
        string='Quantity To Be Produced',
        compute='_compute_qty_remaining',
        store=True,
    )

    qty_initial = fields.Float(
        string='Inıtial Quantity',
        readonly=True,
    )

    image_1920 = fields.Image(
        related='product_tmpl_id.image_1920',
    )

    reference = fields.Char(
        string='Ref',
    )

    report_printed = fields.Boolean(
        string="Yazdırılmış Rapor",
    )

    calculated_prod_qty = fields.Float(
        string='Calculated Quantity to be Produced',
        compute='_compute_calculated_prod_qty',
        store=True,
    )

    @api.depends('product_qty', 'product_id', 'product_uom_id')
    def _compute_calculated_prod_qty(self):
        kg_uom = self.env.ref('uom.product_uom_kgm')
        for production in self:
            if production.product_uom_id == kg_uom:
                if production.product_id.weight:
                    production.calculated_prod_qty = production.product_qty / production.product_id.weight
                else:
                    production.calculated_prod_qty = 0
            else:
                production.calculated_prod_qty = 0

    @api.onchange('product_qty')
    def _onchange_product_qty(self):
        for rec in self:
            if rec.backorder_sequence == 0:
                rec.qty_initial = rec.product_qty

    @api.depends('qty_initial', 'qty_produced')
    def _compute_qty_remaining(self):
        for prop in self:
            prop.qty_remaining = (prop.qty_initial - prop.qty_produced)

    def _get_backorder_mo_vals(self):
        values = super(MrpProduction, self)._get_backorder_mo_vals()
        values['date_planned_start'] = self.date_planned_start
        values['sale_order_ref'] = self.sale_order_ref
        values['parent_client'] = self.parent_client
        values['parent_client_ref'] = self.parent_client_ref
        values['order_client_ref'] = self.order_client_ref
        values['client'] = self.client
        values['qty_initial'] = self.qty_initial
        return values

    def button_mark_done(self):
        for rec in self:
            if rec.picking_type_id.reference_required and not rec.reference:
                raise UserError(_('You must enter the reference before finishing the production!'))
        return super(MrpProduction, self).button_mark_done()
