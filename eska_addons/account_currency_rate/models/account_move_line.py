# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # rate setting methods
    @api.model
    def with_to_currency(self):
        return self

    @api.model
    def with_from_currency(self):
        return self

    @api.model
    def _get_currency_rate_fields(self):
        return [
            "currency_id",
            "company_id",
            "move_id.date",
            "move_id.currency_rate_method",
        ]

    # rate injected methods
    @api.depends(lambda self: self._get_currency_rate_fields())
    def _compute_currency_rate(self):
        # changing this method might result in unexpected results
        for line in self:
            line.currency_rate = line.with_to_currency().env['res.currency']._get_conversion_rate(
                from_currency=line.company_currency_id,
                to_currency=line.currency_id,
                company=line.company_id,
                date=line.move_id.date or fields.Date.context_today(line),
            )

    def copy_data(self, default=None):
        res = super(AccountMoveLine, self).copy_data(default=default)
        for values in res:
            if self._context.get('exchange') and not values['amount_currency']:
                values.pop('currency_id')
        return res
