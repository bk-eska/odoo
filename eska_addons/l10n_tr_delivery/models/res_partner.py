# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_tr_is_transporter = fields.Boolean(
        string='Is Transport Company',
        help='Specify if this is a transport company. Used in E-Despatch.',
    )

    l10n_tr_is_driver = fields.Boolean(
        string='Is a Driver',
        help='Specify if this is a driver. Used in E-Despatch.',
    )
