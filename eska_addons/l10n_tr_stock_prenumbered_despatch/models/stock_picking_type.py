# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PickingType(models.Model):
    _inherit = 'stock.picking.type'

    l10n_tr_despatch_number_sequence = fields.Many2one(
        comodel_name='ir.sequence',
        string='Printed Despatch Number Sequence',
        help='This is used to number printed despatches',
    )

    l10n_tr_despatch_auto_number = fields.Boolean(
        string='Auto Number',
        help='Gives auto number on validate'
    )

    l10n_tr_use_document = fields.Boolean(
        related='company_id.l10n_tr_use_document',
    )
