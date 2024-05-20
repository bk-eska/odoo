# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CurrencyRateMixin(models.AbstractModel):
    _name = 'currency.rate.mixin'
    _description = 'Currency Rate Mixin'

    @api.depends('currency_id', 'company_currency_id')
    def _compute_use_currency_rate(self):
        for rec in self:
            rec.use_currency_rate = rec.currency_id != rec.company_currency_id \
                if rec.currency_id else False

    @api.depends('currency_rate_method')
    def _compute_use_currency_rate_method(self):
        for rec in self:
            rec.use_currency_rate_method = len(
                rec._fields['currency_rate_method'].get_values(self.env)) > 1

    @api.model
    def _get_currency_rate_fields(self):
        return [
            "currency_id",
            "company_id",
            "currency_date",
            "currency_rate_method",
        ]

    @api.model
    def _get_amount_company_currency_fields(self):
        return self._get_currency_rate_fields() + ['amount']

    @api.depends(lambda self: self._get_currency_rate_fields())
    def _compute_currency_rate(self):
        for move in self:
            currency = move.with_from_currency().currency_id
            move.currency_rate = currency.with_context(
                date=move.currency_date or fields.Date.context_today(self),
                company_id=move.company_id.id,
            ).rate
            move.currency_inverse_rate = \
                move.currency_rate and (1.0 / move.currency_rate)

    currency_date = fields.Date(
        string="Currency Date",
    )

    use_currency_rate = fields.Boolean(
        'Use Currency Rate',
        compute='_compute_use_currency_rate',
    )

    use_currency_rate_method = fields.Boolean(
        'Use Conversion Method',
        compute='_compute_use_currency_rate_method',
    )

    currency_rate_method = fields.Selection(
        string="Conversion Method",
        selection=[
            ('default', 'Default Rate'),
        ],
        required=True,
        default='default',
    )

    currency_rate = fields.Float(
        string='Currency Rate',
        digits='Currency Rate',
        compute='_compute_currency_rate',
    )

    currency_inverse_rate = fields.Float(
        string='Currency Inverse Rate',
        digits='Currency Inverse Rate',
        compute='_compute_currency_rate',
    )

    use_inverse_rate = fields.Boolean(
        string='Use Inverse Rate',
        compute='_compute_use_inverse_rate',
    )

    @api.depends('use_currency_rate')
    def _compute_use_inverse_rate(self):
        self.use_inverse_rate = self.user_has_groups(
            'account_currency_rate.group_show_currency_rate_inverse')

    # rate setting methods
    @api.model
    def with_to_currency(self):
        return self

    @api.model
    def with_from_currency(self):
        return self
