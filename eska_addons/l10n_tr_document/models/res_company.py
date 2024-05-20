# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_tr_use_document = fields.Boolean(
        string="Turkey Document Fields",
        help="Use document features compliant with Turkey localization"
    )

    @api.onchange('country_id')
    def _onchange_company(self):
        self.l10n_tr_use_document = self.country_id.code == "TR"
