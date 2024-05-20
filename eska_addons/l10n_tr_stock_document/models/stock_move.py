# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    l10n_tr_use_document = fields.Boolean(
        related='company_id.l10n_tr_use_document',
    )

    l10n_tr_document_number = fields.Char(
        string='Document Number',
        related='picking_id.l10n_tr_document_number',
    )
