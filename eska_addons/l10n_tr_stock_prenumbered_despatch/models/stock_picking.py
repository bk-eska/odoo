# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _get_default_number_sequence(self):
        return self.env['stock.picking.type'].browse(
            self._context.get('default_picking_type_id')).l10n_tr_despatch_number_sequence

    l10n_tr_despatch_number_sequence = fields.Many2one(
        comodel_name='ir.sequence',
        string='Despatch Number Sequence',
        help='Printed Despatch Number Sequence',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        default=_get_default_number_sequence,
    )

    def action_assign_number(self):
        for pick in self:
            if pick.l10n_tr_despatch_number_sequence:
                pick.l10n_tr_document_number = pick.l10n_tr_despatch_number_sequence.with_context(
                    ir_sequence_date=pick.scheduled_date,
                    ir_sequence_date_range=pick.scheduled_date)._next()

    def _action_done(self):
        for pick in self.filtered(lambda l: l.l10n_tr_use_document):
            if pick.picking_type_code != 'incoming' and \
                    pick.l10n_tr_document_type == 'printed' and \
                    pick.picking_type_id.l10n_tr_despatch_auto_number and \
                    not pick.l10n_tr_document_number:
                if not pick.l10n_tr_despatch_number_sequence:
                    pick.l10n_tr_despatch_number_sequence = \
                        pick.picking_type_id.l10n_tr_despatch_number_sequence
                pick.action_assign_number()
        return super()._action_done()
