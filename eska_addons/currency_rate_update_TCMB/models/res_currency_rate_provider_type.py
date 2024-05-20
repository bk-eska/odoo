# Copyright 2017 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResCurrencyRateProviderType(models.Model):
    _name = 'res.currency.rate.provider.type'
    _description = 'Currency Rate Provider Currency Types'

    provider_id = fields.Many2one(
        comodel_name='res.currency.rate.provider',
        string='Service',
        required=True,
    )

    rate_type = fields.Selection(
        [
            ('ForexBuying', 'Forex Buy'),
            ('ForexSelling', 'Forex Sell'),
            ('BanknoteBuying', 'Banknote Buy'),
            ('BanknoteSelling', 'Banknote Sell'),
        ],
        string='Rate Type', required=True)

    currency_rate_type_id = fields.Many2one(
        comodel_name='res.currency.rate.type',
        string='Currency Rate Type',
    )
