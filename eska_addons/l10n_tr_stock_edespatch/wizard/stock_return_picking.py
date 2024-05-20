# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    l10n_tr_return_method = fields.Selection(
        selection=[
            ('create', 'Create a return'),
            ('link', 'Link to an already received E-Despatch'),
        ],
        default='create',
        string='Return Method',
        required=True,
        help='Choose how you want to process this return.',
    )

    l10m_tr_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        readonly=True,
    )

    l10n_tr_link_picking_id = fields.Many2one(
        comodel_name='stock.picking',
        string='E-Despatch To Link',
    )

    @api.model
    def default_get(self, fields):
        res = super(StockReturnPicking, self).default_get(fields)
        active_id = self._context.get('active_id', False)
        if active_id:
            picking = self.env['stock.picking'].browse(active_id)
            res.update({'l10m_tr_partner_id': picking.partner_id.id})
            if picking.l10n_tr_document_type == 'edespatch':
                res.update({'l10n_tr_return_method': 'link'})
        return res

    def _link_returns(self):
        new_picking = self.l10n_tr_link_picking_id
        picking_type_id = self.picking_id.picking_type_id.return_picking_type_id.id or self.picking_id.picking_type_id.id
        new_picking.write({
            'move_ids': [],
            'picking_type_id': picking_type_id,
            'state': 'draft',
            'origin': _("Return of %s") % self.picking_id.name,
            'location_id': self.picking_id.location_dest_id.id,
            'location_dest_id': self.location_id.id})
        self.l10n_tr_link_picking_id.message_post_with_view(
            'mail.message_origin_link',
            values={
                'self': new_picking,
                'origin': self.picking_id
            },
            subtype_id=self.env.ref('mail.mt_note').id,
        )
        returned_lines = 0
        for return_line in self.product_return_moves:
            if not return_line.move_id:
                raise UserError(_(
                    "You have manually created product lines, please delete them to proceed."))
            if return_line.quantity:
                returned_lines += 1
                vals = self._prepare_move_default_values(return_line,
                                                         new_picking)
                r = return_line.move_id.copy(vals)
                vals = {}

                move_orig_to_link = return_line.move_id.move_dest_ids.mapped(
                    'returned_move_ids')
                move_dest_to_link = return_line.move_id.move_orig_ids.mapped(
                    'returned_move_ids')
                vals['move_orig_ids'] = [(4, m.id) for m in
                                         move_orig_to_link | return_line.move_id]
                vals['move_dest_ids'] = [(4, m.id) for m in
                                         move_dest_to_link]
                r.write(vals)
        if not returned_lines:
            raise UserError(
                _("Please specify at least one non-zero quantity."))

        new_picking.action_confirm()
        new_picking.action_assign()
        return new_picking.id, picking_type_id

    def _create_returns(self):
        if self.l10n_tr_return_method == 'link':
            return self._link_returns()
        else:
            picking_id, pick_type_id = \
                super(StockReturnPicking, self)._create_returns()
            self.env['stock.picking'].browse([picking_id])._set_edespatch_vals()
            return picking_id, pick_type_id

