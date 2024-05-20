# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import odoo

from odoo import _, api, models
from odoo.exceptions import ValidationError
from odoo.addons.iap.tools.iap_tools import iap_jsonrpc

ESKA_ENDPOINT = "https://iap.eskayazilim.com.tr"


class OnlineBankStatementProvider(models.Model):
    _inherit = "online.bank.statement.provider"

    @api.model
    def _get_available_services(self):
        return super()._get_available_services() + [
            ("vomsis", "Vomsis (provided by Eska)"),
        ]

    def _obtain_statement_data(self, date_since, date_until):
        if self.service != "vomsis":
            return super()._obtain_statement_data(date_since, date_until)
        if not self.account_number:
            raise ValidationError(_("Account number is not specified!"))
        account = self.env['iap.account'].get_company_account(
            'vomsis', self.company_id)
        params = {
            'version': odoo.release.major_version,
            'account_token': account.account_token,
            'account_number': self.account_number,
            'begin': date_since.strftime("%Y-%m-%d %H:%M:%S"),
            'end': date_until.strftime("%Y-%m-%d %H:%M:%S"),
        }
        result = iap_jsonrpc(
            ESKA_ENDPOINT + '/iap/vomsis/1/get_transaction_data/',
            params=params, timeout=120)
        lines = []
        balances = {}
        for line in result['lines']:
            if 'partner_vat' in line and line['partner_vat']:
                partner = self.env['res.partner'].search([
                    ('vat', 'ilike', line['partner_vat']),
                ], order='parent_id DESC', limit=1)
                if partner:
                    line['partner_id'] = partner.id
                line.pop('partner_vat')
            lines.append(line)
        if lines:
            balances = result['balances']
        return lines, balances
