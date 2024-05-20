# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    l10n_tr_einvoice_send = fields.Boolean(
        string="Send in E-Invoices",
    )
