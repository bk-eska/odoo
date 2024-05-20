# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    l10n_tr_edespatch_enabled = fields.Boolean(
        string='E-Despatch User',
        related='warehouse_id.company_id.l10n_tr_edespatch_enabled'
    )

    l10n_tr_edespatch_sender_id = fields.Many2one(
        comodel_name='l10n_tr.edespatch.sender',
        string='E-Despatch Sender',
    )

    l10n_tr_edespatch_sequence = fields.Many2one(
        comodel_name='ir.sequence',
        string='E-Despatch Number Sequence',
    )

    l10n_tr_edespatch_postbox_ids = fields.One2many(
        comodel_name='l10n_tr.edespatch.postbox',
        inverse_name='picking_type_id',
        string='Postboxes',
        help='Postboxes related with this picking type.',
    )
