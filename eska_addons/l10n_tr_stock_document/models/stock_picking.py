# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.osv import expression
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _rec_names_search = ['name','l10n_tr_document_number','origin']

    l10n_tr_use_document = fields.Boolean(
        related='company_id.l10n_tr_use_document',
    )

    l10n_tr_document_type = fields.Selection(
        selection=[
            ('printed', 'Printed Despatch'),
            ('invoice', 'Despatch Invoice'),
        ],
        string='Document Type',
        required=True,
        default='printed',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
    )

    l10n_tr_document_number = fields.Char(
        string='Document Number',
        index=True,
        copy=False,
    )

    l10n_tr_date_despatch = fields.Datetime(
        string='Actual Despatch Date',
        copy=False,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
    )

    def name_get(self):
        res = []
        for picking in self:
            name = picking.name
            if picking.l10n_tr_document_number:
                name += " - " + picking.l10n_tr_document_number
            if picking.origin:
                name += " (" + picking.origin + ")"
            res.append((picking.id, name))
        return res

    def _action_done(self):
        for rec in self.filtered(lambda x: x.l10n_tr_use_document):
            if rec.picking_type_code in ['outgoing', 'internal', 'incoming'] \
                    and rec.picking_type_id.l10n_tr_document_number_required \
                    and rec.l10n_tr_document_type == 'printed' \
                    and not rec.l10n_tr_document_number:
                raise UserError(_('Please enter document number!'))
        return super(StockPicking, self)._action_done()
