# Copyright 2024 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def check_vat_tr(self, vat):
        if vat in ["11111111111", "2222222222"]:
            return True
        return super(ResPartner, self).check_vat_tr(vat)
