# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    @api.model
    def _get_third_party_checks_country_codes(self):
        return super()._get_third_party_checks_country_codes() + ["TR"]
