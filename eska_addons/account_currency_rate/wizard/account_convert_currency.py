# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tests import Form


class AccountConvertCurrency(models.TransientModel):
    _inherit = 'currency.rate.mixin'
    _name = 'account.convert.currency'
    _description = 'Change Currency'

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Destination Currency',
        required=True,
        help="Select a currency to apply"
    )

    company_currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Company Currency',
        readonly=True,
    )

    currency_date = fields.Date(
        string='Currency Date',
        readonly=True,
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        readonly=True,
    )

    def get_default_vals(self, object):
        return {
            'currency_date': object.currency_date,
            'currency_id': object.currency_id.id,
            'company_currency_id': object.company_currency_id.id,
            'company_id': object.company_id.id,
            'currency_rate_method': object.currency_rate_method,
        }

    @api.model
    def default_get(self, default_fields):
        res = super(AccountConvertCurrency, self).default_get(
            default_fields)
        active_id = self._context.get('active_id', False)
        if active_id:
            move = self.env['account.move'].browse(active_id)
            res.update(self.get_default_vals(move))
        return res

    def set_move_vals(self, move):
        move.currency_id = self.currency_id
        if move.currency_id != self.company_currency_id:
            move.currency_rate_method = self.currency_rate_method

    def convert_currency(self):
        move = self.env['account.move'].browse(
            self._context['active_id'])
        move2 = self.with_to_currency().env['account.move'].browse(
            self._context['active_id'])
        from_currency = move2.with_from_currency().currency_id
        move_form = Form(move)
        if self.currency_id != move.currency_id:
            for line_no in range(len(move_form.invoice_line_ids)):
                with move_form.invoice_line_ids.edit(line_no) as line_form:
                        line_form.price_unit = from_currency._convert(
                            line_form.price_unit, self.currency_id,
                            move.company_id, self.currency_date)
            self.set_move_vals(move_form)
        move_form.save()
        return {'type': 'ir.actions.act_window_close'}
