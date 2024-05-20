# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import functools
import psycopg2

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import mute_logger


class L10nTrEdespatchMerge(models.TransientModel):
    _name = 'l10n_tr.edespatch.match'
    _description = 'Match E-Despatch'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
    )

    src_picking_id = fields.Many2one(
        comodel_name='stock.picking',
        string='Src Picking',
    )

    picking_id = fields.Many2one(
        comodel_name='stock.picking',
        string='Picking',
    )

    @api.model
    def default_get(self, fields):
        if len(self.env.context.get('active_ids', list())) > 1:
            raise UserError(_("You may only match one e-despatch at a time."))
        res = super(L10nTrEdespatchMerge, self).default_get(fields)
        picking = self.env['stock.picking'].browse(
            self.env.context.get('active_id'))
        if picking:
            res.update({
                'src_picking_id': picking.id,
                'partner_id': picking.partner_id.id,
            })
        return res

    @api.model
    def _update_reference_fields(self, src_picking, dst_picking):
        def update_records(model, src, field_model='model', field_id='res_id'):
            Model = self.env[model] if model in self.env else None
            if Model is None:
                return
            records = Model.sudo().search([(field_model, '=', 'stock.picking'), (field_id, '=', src.id)])
            try:
                with mute_logger('odoo.sql_db'), self._cr.savepoint():
                    records.sudo().write({field_id: dst_picking.id})
                    records.env.flush_all()
            except psycopg2.Error:
                records.sudo().unlink()

        update_records = functools.partial(update_records)

        update_records('ir.attachment', src=src_picking, field_model='res_model')
        update_records('mail.followers', src=src_picking, field_model='res_model')
        update_records('mail.activity', src=src_picking, field_model='res_model')
        update_records('mail.message', src=src_picking)

        records = self.env['ir.model.fields'].sudo().search([('ttype', '=', 'reference')])
        for record in records:
            try:
                Model = self.env[record.model]
                field = Model._fields[record.name]
            except KeyError:
                continue

            if field.compute is not None:
                continue

            records_ref = Model.sudo().search([(record.name, '=', 'stock.picking,%d' % src_picking.id)])
            values = {
                record.name: 'stock.picking,%d' % dst_picking.id,
            }
            records_ref.sudo().write(values)

        self.env.flush_all()

    def edespatch_match(self):
        if self.picking_id.l10n_tr_edespatch_uuid:
            raise UserError(
                _("This picking is already matched with another E-despatch."))
        self.picking_id.write({
            'l10n_tr_document_type': 'edespatch',
            'l10n_tr_document_number': self.src_picking_id.l10n_tr_document_number,
            'l10n_tr_edespatch_uuid': self.src_picking_id.l10n_tr_edespatch_uuid,
            'l10n_tr_edespatch_envelope_uuid': self.src_picking_id.l10n_tr_edespatch_envelope_uuid,
            'l10n_tr_edespatch_response_uuid': self.src_picking_id.l10n_tr_edespatch_response_uuid,
            'l10n_tr_edespatch_state': self.src_picking_id.l10n_tr_edespatch_state,
            'l10n_tr_edespatch_sender_id': self.src_picking_id.l10n_tr_edespatch_sender_id.id,
            'l10n_tr_edespatch_postbox_id': self.src_picking_id.l10n_tr_edespatch_postbox_id.id,
            'l10n_tr_edespatch_sequence': self.src_picking_id.l10n_tr_edespatch_sequence.id,
        })
        self._update_reference_fields(self.src_picking_id, self.picking_id)
        self.sudo().src_picking_id.unlink()
        return {
            'name': _('Matched Picking'),
            'view_type': 'form',
            'view_mode': 'form,tree,calendar',
            'res_model': 'stock.picking',
            'res_id': self.picking_id.id,
            'type': 'ir.actions.act_window',
        }
