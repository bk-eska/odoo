# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit = 'account.account'

    l10n_tr_reflection_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Reflection Account',
    )
