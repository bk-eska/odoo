# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CurrencyRateMixin(models.AbstractModel):
    _inherit = 'currency.rate.mixin'

    @api.model
    def _get_currency_rate_fields(self):
        return super(CurrencyRateMixin, self)._get_currency_rate_fields() \
               + ['currency_rate_type_id']

    currency_rate_method = fields.Selection(
        selection_add=[('rate_type', 'Rate Type')],
        ondelete={'rate_type': 'set default'},
    )

    currency_rate_type_id = fields.Many2one(
        'res.currency.rate.type',
        'Currency Rate Type',
        help="Currency rate type for this payment",
    )

    # rate setting methods
    @api.model
    def with_to_currency(self):
        if self.use_currency_rate and self.currency_rate_method == 'rate_type':
            return self.with_context(
                currency_rate_type_to=self.currency_rate_type_id.id)
        else:
            return super(CurrencyRateMixin, self).with_to_currency()

    @api.model
    def with_from_currency(self):
        if self.use_currency_rate and self.currency_rate_method == 'rate_type':
            return self.with_context(
                currency_rate_type_from=self.currency_rate_type_id.id)
        else:
            return super(CurrencyRateMixin, self).with_from_currency()
