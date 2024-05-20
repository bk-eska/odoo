# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_loyalty_reward(self):
        result = super()._loader_params_loyalty_reward()
        result['search_params']['fields'].append('deposit')
        return result