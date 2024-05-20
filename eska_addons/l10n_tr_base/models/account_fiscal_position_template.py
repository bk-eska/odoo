# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class AccountFiscalPositionTemplate(models.Model):
    _inherit = 'account.fiscal.position.template'

    l10n_tr_fp_code = fields.Char(
        string='Code',
    )

    l10n_tr_fp_type = fields.Selection(
        selection=[
            ('ISTISNA', 'İstisna'),
            ('OZELMATRAH', 'Özel Matrah'),
            ('TEVKIFAT', 'Tevkifat'),
            ('IHRACKAYITLI', 'İhraç Kayıtlı'),
        ],
        string='Type',
        help='Fiscal position type used in Turkey. Do not change!',
    )
