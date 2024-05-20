# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def _get_currency_rate_fields(self):
        return super(AccountMoveLine, self)._get_currency_rate_fields() \
               + ['move_id.custom_rate']

    # rate setting methods
    @api.model
    def with_to_currency(self):
        if self.move_id.currency_rate_method == 'fixed_rate':
            return self.with_context(fixed_rate_to=self.move_id.custom_rate)
        else:
            return super(AccountMoveLine,self).with_to_currency()

    @api.model
    def with_from_currency(self):
        if self.move_id.currency_rate_method == 'fixed_rate':
            return self.with_context(fixed_rate_from=self.move_id.custom_rate)
        else:
            return super(AccountMoveLine,self).with_from_currency()
