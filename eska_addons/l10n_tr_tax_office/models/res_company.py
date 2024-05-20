# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    tax_office_id = fields.Many2one(
        comodel_name='account.tax.office',
        related='partner_id.tax_office_id',
        string="Tax Office",
        readonly=False,
    )
