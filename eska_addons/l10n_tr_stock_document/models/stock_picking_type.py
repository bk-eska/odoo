# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    l10n_tr_use_document = fields.Boolean(
        related='company_id.l10n_tr_use_document',
    )

    l10n_tr_document_number_required = fields.Boolean(
        string='Document Number Required',
        default=True,
    )
