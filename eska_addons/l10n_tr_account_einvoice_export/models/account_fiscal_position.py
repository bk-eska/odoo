# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    l10n_tr_default_export_type = fields.Selection(
        selection=[
            ('TEMELFATURA', 'Mikro İhracat (E-Arşiv)'),
            ('IHRACAT', 'İhracat (E-Fatura)'),
        ],
        string='Default Export Type',
    )
