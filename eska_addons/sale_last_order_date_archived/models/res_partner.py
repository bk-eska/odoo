# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_last_order_domain(self):
        domain = super(ResPartner, self)._get_last_order_domain()
        domain += ['|', ('active', '=', True), ('active', '=', False)]
        return domain
