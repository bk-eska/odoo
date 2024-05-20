# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields
from odoo.osv import expression


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'
    _rec_names_search = ['name', 'l10n_tr_fp_code']

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
    )

    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.l10n_tr_fp_code:
                name = '[%s] %s' % (record.l10n_tr_fp_code, name)
            res.append((record.id, name))
        return res
