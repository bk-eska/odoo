# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    mo_created = fields.Boolean(
        string='MO Created',
        readonly=True,
        copy=False,
    )

    def action_create_mo(self):
        self = self.sudo()
        dest_company_id = self.env['res.company'].search([
            ('intercompany_destination', '=', True)
        ], limit=1)
        if not dest_company_id:
            raise UserError(_('Inter-company destination not found!'))
        picking_type_id = self.env['stock.picking.type'].search([
            ('intercompany_operation', '=', True),
            ('company_id', '=', dest_company_id.id),
        ], limit=1)
        if not picking_type_id:
            raise UserError(_('Inter-company operation type not found!'))
        for order in self:
            order_count = 0
            if not order.commitment_date:
                raise UserError(_('Commitment date is required for MO creating!'))
            for line in order.order_line.filtered(lambda l: not l.mo_id):
                bom_id = self.env['mrp.bom'].search([
                    ('active', '=', True),
                    ('product_tmpl_id', '=', line.product_id.product_tmpl_id.id),
                    ('company_id', '=', dest_company_id.id),
                    '|',
                    ('product_id', '=', line.product_id.id),
                    ('product_id', '=', False),
                ], limit=1)
                if not bom_id:
                    return
                    # raise UserError(_('BoM not found for product %s in company %s!'
                    #                   % (line.product_id.name, dest_company_id.name)))

                client = ''
                parent_client = ''
                parent_client_ref = ''
                order_client_ref = ''
                if order.company_id.id == 1: # Yavuz Pres ise
                    client = order.partner_id.name
                    order_client_ref = order.client_order_ref
                elif order.company_id.id == 2: # Teknotel ise
                    client = order.company_id.name
                    parent_client = order.partner_id.name
                    parent_client_ref = order.client_order_ref

                mo_id = self.env['mrp.production'].create({
                    'sale_order_ref': order.name,
                    'sale_order_line_id': line.id,
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_id.uom_id.id,
                    'bom_id': bom_id.id,
                    'product_qty': line.product_uom_qty,
                    'date_deadline': order.commitment_date - relativedelta(days=2) if order.commitment_date else False,
                    'date_planned_start': order.commitment_date - relativedelta(days=3) if order.commitment_date else False,
                    'date_planned_finished': order.commitment_date - relativedelta(days=2) if order.commitment_date else False,
                    'user_id': False,
                    'company_id': dest_company_id.id,
                    'client': client,
                    'parent_client': parent_client,
                    'parent_client_ref': parent_client_ref,
                    'order_client_ref': order_client_ref,
                    'date_source_order': order.date_order,
                    'picking_type_id': picking_type_id.id,
                    'location_src_id': picking_type_id.default_location_src_id.id,
                    'location_dest_id': picking_type_id.default_location_dest_id.id,
                })
                line.mo_id = mo_id
                order_count += 1
            if order_count > 0:
                order.mo_created = True
            order.message_post(body=_('%s manufacturing orders have been created.' % order_count))
