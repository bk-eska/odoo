# Copyright 2021 Eska Technology LLC (www.eskaweb.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    collection_id = fields.Many2one(
        comodel_name='collection.order',
        string='Collection Order',
    )

    collection_line_id = fields.Many2one(
        comodel_name='collection.order.line',
        string='Collection Order Line',
    )

    transfer_collection_id = fields.Many2one(
        comodel_name='collection.order',
        string='Transfer Collection Order',
    )

    document = fields.Binary(
        string='Document',
        attachment=True,
    )

    filename = fields.Char()

