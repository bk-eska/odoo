# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    # rate setting methods
    @api.model
    def with_to_currency(self):
        if self.currency_rate_method == 'fixed_rate':
            return self.with_context(fixed_rate_to=self.custom_rate)
        else:
            return super(AccountPayment, self).with_to_currency()

    @api.model
    def with_from_currency(self):
        if self.currency_rate_method == 'fixed_rate':
            return self.with_context(fixed_rate_from=self.custom_rate)
        else:
            return super(AccountPayment, self).with_from_currency()

    # overridden
    @api.model
    def _get_trigger_fields_to_synchronize(self):
        res = super()._get_trigger_fields_to_synchronize()
        return res + ('custom_rate',)
