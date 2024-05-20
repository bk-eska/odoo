# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields
from odoo.osv import expression


class HrOccupation(models.Model):
    _description = "Occupation"
    _name = 'hr.occupation'
    _order = "code, name"

    name = fields.Char(
        string='Name',
        required=True,
    )

    code = fields.Char(
        string='Code',
        required=True,
    )

    def name_get(self):
        result = []
        for record in self:
            if record.code:
                result.append((record.id, '[' +
                               record.code + '] ' + record.name))
            else:
                result.append((record.id, record.name))
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []

        if operator == 'ilike' and not (name or '').strip():
            domain = []
        else:
            connector = '&' if operator in expression.NEGATIVE_TERM_OPERATORS else '|'
            domain = [connector, ('code', operator, name), ('name', operator, name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
