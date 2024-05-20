# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class ResCurrencyRate(models.Model):
    _inherit = "res.currency.rate"
    _order = "name desc, currency_rate_type_id"

    currency_rate_type_id = fields.Many2one(
        'res.currency.rate.type',
        'Currency Rate Type',
    )

    _sql_constraints = [
        ('unique_name_per_day', 'CHECK(1=1)', 'Constraint disabled!'),
    ]

    @api.constrains('name', 'currency_id', 'company_id',
                    'currency_rate_type_id')
    def _check_unique_rate_per_day_per_type(self):
        for rate in self:
            if(self.search([
                ('id', '!=', rate.id),
                ('name', '=', rate.name),
                ('currency_id', '=', rate.currency_id.id),
                ('company_id', '=', rate.company_id.id),
                ('currency_rate_type_id', '=', rate.currency_rate_type_id.id),
             ])):
                raise ValidationError(
                    _("Only one currency rate per type per day allowed!"))
