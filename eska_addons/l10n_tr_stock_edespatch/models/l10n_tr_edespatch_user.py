# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class L10nTrEdespatchUser(models.Model):

    _name = 'l10n_tr.edespatch.user'
    _description = 'E-Despatch Registered Users'
    _order = "title, identifier"

    identifier = fields.Char(
        string='Identifier',
        required=True,
        index=True,
    )

    alias = fields.Char(
        string='Alias',
        required=True,
        index=True,
    )

    title = fields.Char(
        string='Title',
        required=True,
    )

    type = fields.Char(
        string='Type',
        required=True,
    )

    first_created = fields.Date(
        string='First Created',
    )

    alias_created = fields.Date(
        string='Alias Created',
    )

