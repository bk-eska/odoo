# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CurrencyRateMixin(models.AbstractModel):
    _inherit = 'currency.rate.mixin'

    currency_rate_method = fields.Selection(
        selection_add=[('fixed_rate', 'Fixed Rate')],
        ondelete={'fixed_rate': 'set default'},
    )

    custom_rate = fields.Float(
        string='Custom Rate',
        digits='Currency Rate',
        default=1.0,
    )
    
    custom_inverse_rate = fields.Float(
        string='Custom Inverse Rate',
        digits='Currency Inverse Rate',
        default=1.0,
    )

    @api.onchange('custom_rate')
    def _onchange_inverse_rate(self):
        if self.currency_rate_method == 'fixed_rate':
            self.custom_inverse_rate = self.custom_rate and \
                               (1.0 / self.custom_rate)

    @api.onchange('custom_inverse_rate')
    def _onchange_custom_inverse_rate(self):
        if self.currency_rate_method == 'fixed_rate':
            self.custom_rate = self.custom_inverse_rate and \
                               (1.0 / self.custom_inverse_rate)

    # overridden
    @api.model
    def _get_currency_rate_fields(self):
        return super(CurrencyRateMixin, self)._get_currency_rate_fields() \
               + ['custom_rate']

    # rate setting methods
    @api.model
    def with_to_currency(self):
        if self.use_currency_rate and self.currency_rate_method == 'fixed_rate':
            return self.with_context(fixed_rate_to=self.custom_rate)
        else:
            return super(CurrencyRateMixin, self).with_to_currency()

    @api.model
    def with_from_currency(self):
        if self.use_currency_rate and self.currency_rate_method == 'fixed_rate':
            return self.with_context(fixed_rate_from=self.custom_rate)
        else:
            return super(CurrencyRateMixin, self).with_from_currency()
