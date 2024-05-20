# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re
from odoo import models, _, api
from odoo.exceptions import UserError
from odoo.addons.iap.tools.iap_tools import iap_jsonrpc

import logging

_logger = logging.getLogger(__name__)


class DateRange(models.Model):
    _inherit = "date.range"

    @api.model
    def action_eledger_send(self):
        for range in self:
            if not range.type_id.fiscal_month:
                raise UserError(_('Date Range %s type must be the Fiscal Month!' % range.name))
            if not range.company_id.vat:
                raise UserError(_('Vat not found for company %s!' % range.company_id.name))
            check_move_ids = self.env['account.move'].search([
                ('date', '<=', range.date_end),
                ('date', '>=', range.date_start),
                ('l10n_tr_move_sequence_number', '=', 0),
                ('journal_id.l10n_tr_renumber', '=', True),
                ('state', '=', 'posted'),
                ('company_id', '=', range.company_id.id),
            ])
            for check_move in check_move_ids:
                line_ids = check_move.line_ids.filtered(
                    lambda l: l.debit > 0 or l.credit > 0)
                if line_ids:
                    raise UserError(_('Entry %s is has no sequence! Please renumber or uncheck renumber on the journal!' % check_move.name))
            move_ids = self.env['account.move'].search([
                ('date', '<=', range.date_end),
                ('date', '>=', range.date_start),
                ('l10n_tr_move_sequence_number', '>', 0),
                ('state', '=', 'posted'),
                ('company_id', '=', range.company_id.id),
            ], order='l10n_tr_move_sequence_number')
            ledger = [
                # 'RecordType': 'L',
                range.company_id.vat[2:] if range.company_id.vat[:2] == 'TR' else range.company_id.vat, #Identifier
                '0', #batchID
                range.date_start.strftime('%Y-%m-%d'), #periodCoveredStart
                range.date_end.strftime('%Y-%m-%d'), #periodCoveredEnd
                len(move_ids), #entryHeaderCount
                [], #entryHeader
            ]
            for move in move_ids:
                if move.move_type == 'entry':
                    move_type = _('Account_Entry')
                elif 'receipt' in move.move_type:
                    move_type = _('Receipt')
                else:
                    move_type = _('Invoice')
                move_lines =  move.line_ids.filtered(
                    lambda l: l.l10n_tr_line_sequence_number > 0).sorted(
                    key=lambda l: l.l10n_tr_line_sequence_number)
                move_entry = [
                    # 'RecordType': 'H',
                    move.create_uid.name, #enteredBy
                    move.date.strftime('%Y-%m-%d'), #enteredDate
                    re.sub(r'[\n\t\r|]', '', move.name or ''), #entryNumber
                    move.l10n_tr_move_sequence_number, #entryNumberCounter
                    re.sub(r'[\n\t\r|]', '', move.ref or move_type), #entryComment
                    len(move_lines), #entryDetailCount
                    [], #entryDetail
                ]
                for line in move_lines:
                    if not line.account_id:
                        raise UserError(_(
                            'Account not found for line %s in %s!' % (line.name, move.name)))
                    code = line.account_id.code
                    payment_type = line.journal_id.l10n_tr_payment_type
                    payment_method = False
                    if payment_type == 'cash':
                        payment_method = 'Nakit'
                    elif payment_type == 'bank':
                        payment_method = 'Banka'
                    elif payment_type == 'credit_card':
                        payment_method = 'Kredi Kartı'
                    elif payment_type == 'check':
                        payment_method = 'Çek'
                    elif payment_type == 'promissory':
                        payment_method = 'Senet'

                    document_type = line.move_id.l10n_tr_document_type
                    document_type_desc = document_number = document_date = False
                    if document_type:
                        if document_type == 'other':
                            if line.move_id.l10n_tr_document_type_description:
                                document_type_desc = re.sub(r'[\n\t\r|]', '', line.move_id.l10n_tr_document_type_description)
                            else:
                                raise UserError(_('Document Type Description is required for %s!' % move.name))
                        if line.move_id.l10n_tr_document_number:
                            document_number = re.sub(r'[\n\t\r|]', '', line.move_id.l10n_tr_document_number)
                        else:
                            raise UserError(_('Document Number is required for %s!' % move.name))
                        if line.move_id.l10n_tr_document_number:
                            document_date = line.move_id.l10n_tr_document_date.strftime('%Y-%m-%d')
                        else:
                            raise UserError(_('Document Date is required for %s!' % move.name))

                    line_entry = [
                        # 'RecordType': 'D',
                        code[:3], #accountMainID
                        re.sub(r'[\n\t\r|]', '', line.account_id.group_id.name or line.account_id.name), #accountMainDescription
                        code, #accountSubID
                        re.sub(r'[\n\t\r|]', '', line.account_id.name or ''), #accountSubDescription
                        line.debit if line.debit > 0.0 else line.credit, #amount
                        'D' if line.debit > 0.0 else 'C', #debitCreditCode
                        document_type, #documentType
                        document_type_desc, #documentTypeDescription
                        document_number, #documentNumber
                        document_date, #documentDate
                        re.sub(r'[\n\t\r|]', '', line.move_id.name or ''), #documentReference
                        payment_method, #paymentMethod
                        re.sub(r'[\n\t\r|]', '', line.name or '') , #detailComment
                    ]
                    move_entry[6].append(line_entry)
                ledger[5].append(move_entry)
            account = self.env['iap.account'].get_company_account(
                'foriba', range.company_id)
            params = {
                'account_token': account.account_token,
                'ledger': ledger,
            }
            try:
                endpoint = range.company_id._get_default_endpoint()
                _logger.info("eledger_data_save")
                iap_jsonrpc(endpoint + '/iap/foriba/1/eledger_save/', params=params, timeout=120)
            except Exception as e:
                _logger.info("eledger_data_save failed: %s" % str(e))
                raise UserError(_("eledger_data_save failed for range %s: %s" % (range.name, str(e))))
