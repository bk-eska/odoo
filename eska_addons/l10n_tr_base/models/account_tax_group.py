# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountTaxGroup(models.Model):
    _inherit = 'account.tax.group'

    l10n_tr_tax_type = fields.Many2one(
        comodel_name='l10n_tr.tax.type',
        string='Type',
        help='Tax type used in Turkey. Do not change!',
    )
