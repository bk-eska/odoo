# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    def _get_fp_vals(self, company, position):
        values = super(AccountChartTemplate, self)._get_fp_vals(
            company, position)
        values['l10n_tr_fp_type'] = position.l10n_tr_fp_type
        values['l10n_tr_fp_code'] = position.l10n_tr_fp_code
        return values
