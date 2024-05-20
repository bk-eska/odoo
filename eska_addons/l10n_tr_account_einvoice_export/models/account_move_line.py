# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

_logger = logging.getLogger(__name__)

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    l10n_tr_package_quantity = fields.Integer(
        string='Package Quantity',
    )

    l10n_tr_package_type_id = fields.Many2one(
        string='Package Type',
        comodel_name='stock.package.type',
    )
