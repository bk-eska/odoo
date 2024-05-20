# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class L10n_trTaxType(models.Model):
    _name = 'l10n_tr.tax.type'
    _description = 'Tax Type Category'
    _order = 'code, name'

    name = fields.Char(
        string='Name',
        required=True,
    )

    code = fields.Char(
        string='Code',
        required=True,
    )

    def name_get(self):
        res = []
        for record in self:
            name = '[%s] %s' % (record.code, record.name)
            res.append((record.id, name))
        return res