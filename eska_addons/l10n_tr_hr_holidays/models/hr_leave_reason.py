# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class HRLeaveReason(models.Model):
    _name = "hr.leave.reason"
    _description = "HR Holidays Leave Reason"
    _order = "code, name"

    name = fields.Char(
        string='Name',
        required=True,
    )

    code = fields.Char(
        string='Code',
        required=True,
    )

    description = fields.Text(
        string='Description',
    )

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '(%s) %s' % (rec.code, rec.name)))
        return res