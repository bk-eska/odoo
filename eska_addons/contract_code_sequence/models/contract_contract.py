# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    code = fields.Char(
        copy=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for contract in res:
            if not contract.code:
                contract.code = self.env['ir.sequence'].next_by_code('contract.contract')
        return res
