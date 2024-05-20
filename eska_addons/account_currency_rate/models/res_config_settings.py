# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_show_currency_rate_normal = fields.Boolean(
        "Show currency rate normal",
        implied_group='account_currency_rate.group_show_currency_rate_normal',
        group='base.group_portal,base.group_user,base.group_public',
        compute='_compute_group_show_currency_rate', store=True,
        readonly=False)
    group_show_currency_rate_inverse = fields.Boolean(
        "Show currency rate inverse",
        implied_group='account_currency_rate.group_show_currency_rate_inverse',
        group='base.group_portal,base.group_user,base.group_public',
        compute='_compute_group_show_currency_rate', store=True,
        readonly=False)

    show_currency_rate_selection = fields.Selection([
        ('normal', 'Normal'),
        ('inverse', 'Inverted')], string="Currency Rate Display",
        required=True, default='normal',
        config_parameter='account_currency_rate.show_currency_rate_selection')

    @api.depends('show_currency_rate_selection')
    def _compute_group_show_currency_rate(self):
        for wizard in self:
            wizard.group_show_currency_rate_normal = wizard.show_currency_rate_selection == "normal"
            wizard.group_show_currency_rate_inverse = wizard.show_currency_rate_selection == "inverse"
