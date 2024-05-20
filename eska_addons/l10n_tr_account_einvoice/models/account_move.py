# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import uuid
import pytz
import base64
import zipfile
import io
from hashlib import md5

from datetime import datetime
from dateutil.relativedelta import relativedelta

from lxml import etree
from lxml.etree import DocumentInvalid

import logging

_logger = logging.getLogger(__name__)

from odoo import _, api, fields, models
from odoo.addons.iap.tools.iap_tools import iap_jsonrpc
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo.tools.misc import file_open


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_tr_delivery_type = fields.Selection(
        selection_add=[
            ('einvoice', 'E-Invoice'),
            ('earchive', 'E-Archive'),
        ],
        ondelete={
            'einvoice': 'set default',
            'earchive': 'set default',
        },
    )

    l10n_tr_einvoice_uuid = fields.Char(
        string='UUID',
        readonly=True,
        copy=False,
    )

    l10n_tr_einvoice_envelope_uuid = fields.Char(
        string='Envelope UUID',
        readonly=True,
        copy=False,
        index=True,
    )

    l10n_tr_einvoice_response_uuid = fields.Char(
        string='Response UUID',
        readonly=True,
        copy=False,
        index=True,
    )

    l10n_tr_einvoice_profile = fields.Selection(
        selection=[
            ('TEMELFATURA', 'Temel Fatura'),
            ('TICARIFATURA', 'Ticari Fatura'),
            ('OZELFATURA', 'Özel Fatura'),
            ('KAMU', 'Kamu'),
            ('HKS', 'Hal Tipi'),
            ('ENERJI', 'Enerji'),
        ],
        string='E-Invoice Profile',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    l10n_tr_einvoice_state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('sent', 'Sent'),  # 1000, 1100, 1200, 1210, 1220 +
            ('waiting', 'Waiting Response'),  # kabul, red
            ('failed', 'Failed'),
            ('completed', 'Completed'),  # 1300 open
            ('rejected', 'Rejected'),
        ],
        string='E-Invoice Status',
        copy=False,
    )

    l10n_tr_einvoice_response_type = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        string='E-Invoice Response Type',
        readonly=True,
        copy=False,
    )

    l10n_tr_einvoice_sender_id = fields.Many2one(
        comodel_name='l10n_tr.einvoice.sender',
        string='Sender',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    l10n_tr_einvoice_postbox_id = fields.Many2one(
        comodel_name='l10n_tr.einvoice.postbox',
        string='Postbox',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    l10n_tr_einvoice_sequence = fields.Many2one(
        comodel_name='ir.sequence',
        string='E-Invoice Number Sequence',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    def _get_l10n_tr_default_einvoice_profile(self):
        partner = self.partner_id.commercial_partner_id
        return partner.l10n_tr_default_einvoice_profile or 'TEMELFATURA'

    def _get_l10n_tr_default_einvoice_postbox(self):
        partner = self.partner_id.commercial_partner_id
        if partner.l10n_tr_default_einvoice_postbox:
            return partner.l10n_tr_default_einvoice_postbox
        else:
            if partner.l10n_tr_einvoice_postbox_ids:
                return partner.l10n_tr_einvoice_postbox_ids[0]
        return False

    @api.model
    def _set_einvoice_vals(self):
        if self.company_id and self.partner_id and self.journal_id:
            if self.l10n_tr_delivery_type == 'einvoice':
                if self.move_type == 'out_invoice':
                    partner = self.partner_id.commercial_partner_id
                    self.l10n_tr_einvoice_profile = self._get_l10n_tr_default_einvoice_profile()
                else:
                    self.l10n_tr_einvoice_profile = 'TEMELFATURA'
                if self.move_type in ('out_invoice', 'in_refund'):
                    self.l10n_tr_einvoice_postbox_id = self._get_l10n_tr_default_einvoice_postbox()
                    self.l10n_tr_einvoice_state = self.l10n_tr_einvoice_state or 'draft'
                    self.l10n_tr_einvoice_sequence = \
                        self.journal_id.l10n_tr_einvoice_sequence
                    self.l10n_tr_einvoice_sender_id = \
                        self.journal_id.l10n_tr_einvoice_sender_id
            elif self.l10n_tr_delivery_type == 'earchive':
                self.l10n_tr_einvoice_profile = False
                self.l10n_tr_einvoice_postbox_id = False
                self.l10n_tr_einvoice_state = self.l10n_tr_einvoice_state or 'draft'
                self.l10n_tr_einvoice_sequence = \
                    self.journal_id.l10n_tr_earchive_sequence
                self.l10n_tr_einvoice_sender_id = False
            elif self.l10n_tr_delivery_type == 'printed':
                self.l10n_tr_einvoice_state = False
                self.l10n_tr_einvoice_profile = False
                self.l10n_tr_einvoice_postbox_id = False
                self.l10n_tr_einvoice_sender_id = False
                self.l10n_tr_einvoice_sequence = False

    def _set_l10n_tr_delivery_type(self):
        for rec in self:
            partner = rec.partner_id.commercial_partner_id
            if rec.company_id.l10n_tr_einvoice_enabled and \
                    partner.l10n_tr_einvoice_user:
                rec.l10n_tr_delivery_type = 'einvoice'
            elif rec.company_id.l10n_tr_einvoice_enabled and \
                    rec.move_type == 'out_invoice':
                rec.l10n_tr_delivery_type = 'earchive'
            else:
                rec.l10n_tr_delivery_type = 'printed'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        result = super(AccountMove, self)._onchange_partner_id()
        self._set_l10n_tr_delivery_type()
        self._set_einvoice_vals()
        return result

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        result = super(AccountMove, self)._onchange_journal_id()
        self._set_einvoice_vals()
        return result

    @api.onchange('l10n_tr_delivery_type')
    def _onchange_l10n_tr_delivery_type(self):
        self._set_einvoice_vals()

    @api.model_create_multi
    def create(self, vals_list):
        moves = super(AccountMove, self).create(vals_list)
        for move, vals in zip(moves, vals_list):
            if 'move_type' in vals and vals['move_type'] != 'entry' and \
                    'l10n_tr_delivery_type' not in vals:
                move._set_l10n_tr_delivery_type()
                move._set_einvoice_vals()
        return moves

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        res = super(AccountMove, self).get_view(
            view_id=view_id, view_type=view_type, **options)
        if self._context.get('default_move_type'):
            doc = etree.XML(res['arch'])
            if self._context['default_move_type'] in ('out_invoice', 'in_refund'):
                for node in doc.xpath("//field[@name='l10n_tr_einvoice_sender_id']"):
                    node.set('domain', "[('company_id', '=', company_id)]")
                for node in doc.xpath("//field[@name='l10n_tr_einvoice_postbox_id']"):
                    node.set('domain',
                             "[('partner_id', '=', commercial_partner_id)]")
            else:
                for node in doc.xpath("//field[@name='l10n_tr_einvoice_sender_id']"):
                    node.set('domain',
                             "[('partner_id', '=', commercial_partner_id)]")
                for node in doc.xpath("//field[@name='l10n_tr_einvoice_postbox_id']"):
                    node.set('domain', "[('company_id', '=', company_id)]")
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    def button_draft(self):
        for inv in self:
            if inv.state == 'cancel' and inv.l10n_tr_delivery_type == 'earchive' and \
                    inv.move_type in ['out_invoice', 'in_refund'] and \
                    inv.l10n_tr_einvoice_state != 'draft':
                raise UserError(_('Cannot set cancelled E-archive invoices to draft!'))
        return super(AccountMove, self).button_draft()

    def _post(self, soft=True):
        for rec in self:
            if rec.move_type in ['out_invoice', 'in_refund'] and \
                    rec.l10n_tr_delivery_type in ['einvoice', 'earchive'] and \
                    rec.l10n_tr_einvoice_state in [False, 'draft']:

                if rec.l10n_tr_delivery_type == 'einvoice' and \
                        rec.l10n_tr_einvoice_profile != 'IHRACAT' and \
                        not rec.commercial_partner_id.l10n_tr_einvoice_user:
                    raise UserError(_('Partner is not an E-invoice user!'))
                elif rec.l10n_tr_delivery_type == 'earchive':
                    if rec.commercial_partner_id.l10n_tr_einvoice_user:
                        raise UserError(_('Partner is an E-invoice user!'))
                    if rec.company_id.l10n_tr_earchive_auto_email and \
                            not rec.partner_id.email:
                        raise ValidationError(_(
                            'Customer %s does not have an email!' % rec.partner_id.name
                        ))

                if not rec.l10n_tr_einvoice_sequence:
                    raise UserError(
                        _("Please select an E-invoice sequence!"))
                if not rec.l10n_tr_einvoice_sequence.active:
                    raise UserError(
                        _("E-invoice sequence is not active!"))
                invoice_date = rec.invoice_date or fields.Date.context_today(self)
                later_invoice = rec.search([
                    ('l10n_tr_delivery_type', 'in', ['einvoice', 'earchive']),
                    ('state', '=', 'posted'),
                    ('move_type', 'in', ['out_invoice', 'in_refund']),
                    ('l10n_tr_einvoice_sequence', '=',
                     rec.l10n_tr_einvoice_sequence.id),
                    ('invoice_date', '>', invoice_date)],
                    limit=1,
                )
                if later_invoice:
                    raise UserError(
                        _('Invoice %s is validated on %s after '
                          'this date using this invoice sequence!') %
                        (later_invoice.l10n_tr_document_number,
                         later_invoice.invoice_date))
                rec.l10n_tr_document_number = rec.l10n_tr_einvoice_sequence.with_context(
                    ir_sequence_date=invoice_date,
                    ir_sequence_date_range=invoice_date)._next()

        result = super(AccountMove, self)._post(soft)

        for rec in self:
            if rec.move_type in ['out_invoice', 'in_refund'] and \
                    rec.l10n_tr_delivery_type in ['einvoice', 'earchive'] and \
                    rec.l10n_tr_einvoice_state in [False, 'draft']:
                if rec.l10n_tr_delivery_type == 'einvoice':
                    rec.einvoice_send()
                elif rec.l10n_tr_delivery_type == 'earchive':
                    rec.earchive_send()
        return result

    @api.model
    def _get_xslt_params(self):
        return {}

    @api.model
    def einvoice_attach_pdf(self, ubl, xslt=False):
        try:
            pdf = self.env['ir.actions.reports']._render_qweb_pdf(
                'account.report_invoice', [self.id],
                {'xml': ubl, 'xslt': xslt})[0]
            attachment_vals = {
                'name': self.l10n_tr_document_number + '.pdf',
                'datas': base64.encodebytes(pdf),
                'res_model': 'account.move',
                'res_id': self.id,
                'type': 'binary',
                'company_id': self.company_id.id,
            }
            attachment = self.env['ir.attachment'].create(attachment_vals)
            self.message_post(attachment_ids=[attachment.id])
        except Exception as e:
            _logger.info("einvoice_attach_pdf failed: %s" % str(e))
            pass

    def button_cancel(self):
        for inv in self:
            if inv.l10n_tr_delivery_type == 'einvoice':
                if inv.move_type in ['out_invoice', 'in_refund']:
                    if inv.l10n_tr_einvoice_state in ['sent', 'waiting']:
                        raise UserError(
                            _("You cannot cancel sent E-Invoices! Please wait for invoice to be received."))
        result = super(AccountMove, self).button_cancel()
        for inv in self:
            if inv.l10n_tr_delivery_type == 'earchive' and \
                    inv.move_type == 'out_invoice' and \
                    inv.l10n_tr_einvoice_state == 'completed':
                inv.earchive_cancel()
        return result

    def _reverse_moves(self, default_values_list=None, cancel=False):
        result = super()._reverse_moves(
            default_values_list=default_values_list, cancel=cancel)
        result._set_einvoice_vals()
        return result

    # UBL Methods
    def einvoice_generate_product_xml(self, item, cac, cbc, line):
        if self.move_type == 'out_invoice' and 'product.customerinfo' in self.env:
            bid = self.env['product.customerinfo'].search([
                ('partner_id', '=', self.partner_id.commercial_partner_id.id),
                ('product_id', '=', line.product_id.id),
                ('company_id', '=', self.company_id.id),
            ], limit=1)
            if not bid:
                bid = self.env['product.customerinfo'].search([
                    ('partner_id', '=', self.partner_id.commercial_partner_id.id),
                    ('product_tmpl_id', '=', line.product_id.product_tmpl_id.id),
                    ('company_id', '=', self.company_id.id),
                ], limit=1)
            if bid and bid.product_code:
                bii = etree.SubElement(item,'{%s}BuyersItemIdentification' % cac)
                etree.SubElement(bii, '{%s}ID' % cbc).text = bid.product_code
        if line.product_id.default_code:
            sii = etree.SubElement(item, '{%s}SellersItemIdentification' % cac)
            etree.SubElement(sii, '{%s}ID' % cbc).text = line.product_id.default_code

    @api.model
    def einvoice_generate_invoice_line_note_xml(self, invoice_line, cac, cbc, line):
        # this method will be used to add line note
        return

    @api.model
    def einvoice_generate_order_xml(self, parent, cac, cbc):
        # this method will be used to add order reference
        return

    @api.model
    def einvoice_buyer_party_xml(self, parent, cac, cbc, party):
        # this method will be used to add buyer information
        return

    @api.model
    def einvoice_generate_despatch_xml(self, parent, cac, cbc):
        # this method will be used to add despatch reference
        return

    @api.model
    def einvoice_generate_delivery_xml(self, parent, cac, cbc):
        # this method will be used to add delivery information
        return

    @api.model
    def einvoice_generate_delivery_line_xml(self, parent, line, price_precision,
                                            line_price_unit, cac, cbc):
        # this method will be used to add delivery information
        return

    @api.model
    def einvoice_generate_additional_document_reference_xml(self, parent, cac,
                                                            cbc, invoice_date):
        if self.l10n_tr_delivery_type == 'earchive':
            output = etree.SubElement(parent,
                                      '{%s}AdditionalDocumentReference' % cac)
            etree.SubElement(output, '{%s}ID' % cbc).text = "0000"
            etree.SubElement(output, '{%s}IssueDate' % cbc).text = invoice_date
            etree.SubElement(output,
                             '{%s}DocumentTypeCode' % cbc).text = 'OUTPUT_TYPE'
            output = etree.SubElement(parent,
                                      '{%s}AdditionalDocumentReference' % cac)
            etree.SubElement(output, '{%s}ID' % cbc).text = "KAGIT"
            etree.SubElement(output, '{%s}IssueDate' % cbc).text = invoice_date
            etree.SubElement(output,
                             '{%s}DocumentTypeCode' % cbc).text = 'EREPSENDT'

        xsltref = etree.SubElement(parent,
                                   '{%s}AdditionalDocumentReference' % cac)
        etree.SubElement(xsltref, '{%s}ID' % cbc).text = "1"
        etree.SubElement(xsltref, '{%s}IssueDate' % cbc).text = invoice_date
        etree.SubElement(xsltref, '{%s}DocumentTypeCode' % cbc).text = 'XSLT'
        etree.SubElement(xsltref, '{%s}DocumentType' % cbc).text = 'XSLT'
        attachment = etree.SubElement(xsltref, '{%s}Attachment' % cac)

        report = self.env['ir.actions.reports'].search(
            [('report_name', '=', 'account.report_invoice')], limit=1)
        xslt = report._render_qweb_html(report.report_name, [self.id], {'get_xslt': True})[0]
        if not xslt:
            raise ValidationError(_('Cannot find XSLT for this invoice.'))
        else:
            etree.SubElement(attachment,
                             '{%s}EmbeddedDocumentBinaryObject' % cbc,
                             attrib={'characterSetCode': 'UTF-8',
                                     'encodingCode': 'Base64',
                                     'filename': '%s.xslt' % self.l10n_tr_document_number,
                                     'mimeCode': 'application/xml'}
                             ).text = base64.b64encode(xslt).decode()

    @api.model
    def einvoice_accounting_customer_party_xml(self, einvoice, cac, cbc,
                                               party, accounting_party):
        customer = etree.SubElement(einvoice,
                                    '{%s}AccountingCustomerParty' % cac)
        branch = self.partner_id if party != self.partner_id and \
                                    self.partner_id.type == 'invoice' else False
        party.ubltr_generate_party_xml(
            'customer', customer, cac, cbc,
            party.l10n_tr_party_identifiers, accounting_party, branch=branch)
        self.einvoice_buyer_party_xml(einvoice, cac, cbc, party)

    @api.model
    def einvoice_generate_currency_note_xml(self, parent, cbc):
        amount_total_words = self.currency_id.amount_to_text(self.amount_total)
        etree.SubElement(parent, '{%s}Note' % cbc).text = _(
            'Only: ') + '%s' % amount_total_words
        if self.currency_id != self.company_id.currency_id:
            if self.amount_total:
                rate = abs(self.amount_total_signed) / self.amount_total
            else:
                rate = 1 / self.currency_id.with_context(
                    date=self.invoice_date or fields.Date.context_today(self)).rate
            etree.SubElement(parent, '{%s}Note' % cbc).text = \
                _('Currency Rate: 1 %s = %.4f %s') % \
                (self.currency_id.name, rate, self.company_id.currency_id.name)

    @api.model
    def ubltr_generate_note_xml(self, parent, cbc, field):
        if field:
            for narration in field.splitlines():
                etree.SubElement(parent, '{%s}Note' % cbc).text = narration

    @api.model
    def einvoice_get_invoice_lines(self):
        return self.invoice_line_ids.filtered(lambda l: l.display_type == 'product')

    @api.model
    def einvoice_generate_ubl_xml_etree(self):
        account_precision = self.env['decimal.precision'].precision_get(
            'Account')
        price_precision = self.env['decimal.precision'].precision_get(
            'Product Price')
        uom_precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        discount_precision = self.env['decimal.precision'].precision_get(
            'Discount')
        if not self.l10n_tr_einvoice_uuid:
            self.l10n_tr_einvoice_uuid = str(uuid.uuid4())
        xmlns = 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2'
        cac = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
        cbc = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
        ext = 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2'
        einvoice = etree.Element('{%s}Invoice' % xmlns,
                                 nsmap={
                                     None: xmlns,
                                     'cac': cac,
                                     'cbc': cbc,
                                     'ext': ext
                                 })
        etree.SubElement(einvoice, '{%s}UBLVersionID' % cbc).text = '2.1'
        etree.SubElement(einvoice, '{%s}CustomizationID' % cbc).text = 'TR1.2'

        fp = self.fiscal_position_id
        if self.l10n_tr_delivery_type == 'earchive':
            etree.SubElement(einvoice,
                             '{%s}ProfileID' % cbc).text = 'EARSIVFATURA'
        else:
            etree.SubElement(einvoice,
                             '{%s}ProfileID' % cbc).text = self.l10n_tr_einvoice_profile
        etree.SubElement(einvoice,
                         '{%s}ID' % cbc).text = self.l10n_tr_document_number or ''
        etree.SubElement(einvoice, '{%s}CopyIndicator' % cbc).text = 'false'
        etree.SubElement(einvoice, '{%s}UUID' % cbc).text = self.l10n_tr_einvoice_uuid
        if self.invoice_date:
            invoice_date = self.invoice_date
        else:
            invoice_date = datetime.now(pytz.timezone('Europe/Istanbul'))
        invoice_date = invoice_date.strftime("%Y-%m-%d")
        if self.confirm_date:
            invoice_time = self.confirm_date.replace(tzinfo=pytz.utc).astimezone(
                pytz.timezone('Europe/Istanbul')).strftime("%H:%M:%S")
        else:
            invoice_time = datetime.now(pytz.timezone('Europe/Istanbul')).strftime("%H:%M:%S")
        etree.SubElement(einvoice, '{%s}IssueDate' % cbc).text = invoice_date
        if self.l10n_tr_delivery_type == 'earchive':
            etree.SubElement(einvoice,
                             '{%s}IssueTime' % cbc).text = invoice_time
        invoice_type_code = etree.SubElement(einvoice,
                                             '{%s}InvoiceTypeCode' % cbc)
        if self.move_type == 'out_invoice':
            if fp and fp.l10n_tr_fp_type == 'ISTISNA':
                invoice_type_code.text = 'ISTISNA'
            elif fp and fp.l10n_tr_fp_type == 'OZELMATRAH':
                invoice_type_code.text = 'OZELMATRAH'
            elif fp and fp.l10n_tr_fp_type == 'TEVKIFAT':
                invoice_type_code.text = 'TEVKIFAT'
            elif fp and fp.l10n_tr_fp_type == 'IHRACKAYITLI':
                invoice_type_code.text = 'IHRACKAYITLI'
            elif self.l10n_tr_einvoice_profile == 'ENERJI':
                invoice_type_code.text = 'SARJ'
            else:
                invoice_type_code.text = 'SATIS'
        else:  # in_refund
            if fp and fp.l10n_tr_fp_type == 'TEVKIFAT':
                invoice_type_code.text = 'TEVKIFATIADE'
            else:
                invoice_type_code.text = 'IADE'
            if self.l10n_tr_delivery_type == 'einvoice' and \
                    self.l10n_tr_einvoice_profile != 'TEMELFATURA':
                raise UserError(_(
                    "Return invoices can be only be used with TEMELFATURA profile!"))

        self.einvoice_generate_currency_note_xml(einvoice, cbc)
        notes = self.env["ir.fields.converter"].html_to_text(self.narration)
        self.ubltr_generate_note_xml(einvoice, cbc, notes)

        etree.SubElement(einvoice,
                         '{%s}DocumentCurrencyCode' % cbc).text = self.currency_id.name

        if self.currency_id != self.company_id.currency_id:
            etree.SubElement(einvoice,
                             '{%s}TaxCurrencyCode' % cbc).text = self.currency_id.name
            etree.SubElement(einvoice,
                             '{%s}PricingCurrencyCode' % cbc).text = self.currency_id.name

        invoice_line_ids = self.einvoice_get_invoice_lines()

        etree.SubElement(einvoice, '{%s}LineCountNumeric' % cbc).text = str(
            len(invoice_line_ids))

        self.einvoice_generate_order_xml(einvoice, cac, cbc)

        if self.move_type == 'in_refund' and self.reversed_entry_id:
            reference = etree.SubElement(einvoice,
                                         '{%s}BillingReference' % cac)
            inv_ref = etree.SubElement(reference,
                                       '{%s}InvoiceDocumentReference' % cac)
            etree.SubElement(inv_ref, '{%s}ID' % cbc).text = \
                self.reversed_entry_id.l10n_tr_document_number
            etree.SubElement(inv_ref,'{%s}IssueDate' % cbc).text = \
                self.reversed_entry_id.invoice_date.strftime("%Y-%m-%d")
            etree.SubElement(inv_ref, '{%s}DocumentTypeCode' % cbc).text = 'IADE'

        self.einvoice_generate_despatch_xml(einvoice, cac, cbc)

        if self.ref:
            xsltref = etree.SubElement(einvoice,
                                       '{%s}OriginatorDocumentReference' % cac)
            etree.SubElement(xsltref, '{%s}ID' % cbc).text = self.ref
            etree.SubElement(xsltref, '{%s}IssueDate' % cbc).text = invoice_date

        self.einvoice_generate_additional_document_reference_xml(einvoice, cac,
                                                                 cbc,
                                                                 invoice_date)

        if self.move_type == 'out_invoice':
            accounting_party = 'company'
        else:
            accounting_party = 'partner'

        commercial_partner = self.partner_id.commercial_partner_id

        company = etree.SubElement(einvoice,
                                   '{%s}AccountingSupplierParty' % cac)
        self.company_id.partner_id.ubltr_generate_party_xml(
            'company', company, cac, cbc,
            commercial_partner.l10n_tr_party_identifiers, accounting_party,
            branch=self.journal_id.l10n_tr_branch_id)

        self.einvoice_accounting_customer_party_xml(einvoice, cac, cbc,
                                                    commercial_partner,
                                                    accounting_party)

        self.einvoice_generate_delivery_xml(einvoice, cac, cbc)

        for bank_account in self.company_id.bank_ids.filtered(lambda b: b.l10n_tr_einvoice_send):
            bank_account_currency = bank_account.currency_id or self.company_id.currency_id
            # Türkiye'ye kesilen faturalar TL ödenmek zorunda
            if (commercial_partner.country_id.code == 'TR' and bank_account_currency.name == 'TRY') or \
                    (commercial_partner.country_id.code != 'TR' and bank_account_currency == self.currency_id):
                means = etree.SubElement(einvoice, '{%s}PaymentMeans' % cac)
                etree.SubElement(means, '{%s}PaymentMeansCode' % cbc).text = "42"
                etree.SubElement(means, '{%s}PaymentDueDate' % cbc).text = \
                    self.invoice_date_due.strftime("%Y-%m-%d")
                if bank_account.bank_id:
                    etree.SubElement(means, '{%s}InstructionNote' % cbc).text = bank_account.bank_id.name
                payee_account = etree.SubElement(means, '{%s}PayeeFinancialAccount' % cac)
                etree.SubElement(payee_account, '{%s}ID' % cbc).text = bank_account.acc_number
                etree.SubElement(payee_account, '{%s}CurrencyCode' % cbc).text = bank_account_currency.name
                etree.SubElement(payee_account, '{%s}PaymentNote' % cbc).text = bank_account.acc_holder_name or bank_account.partner_id.name
                if bank_account.bank_id and bank_account.bank_id.bic:
                    inst_branch = etree.SubElement(payee_account, '{%s}FinancialInstitutionBranch' % cac)
                    inst = etree.SubElement(inst_branch, '{%s}FinancialInstitution' % cac)
                    etree.SubElement(inst, '{%s}Name' % cbc).text = bank_account.bank_id.bic

        terms = etree.SubElement(einvoice, '{%s}PaymentTerms' % cac)
        if self.invoice_payment_term_id:
            if self.invoice_payment_term_id.note:
                term = self.env["ir.fields.converter"].html_to_text(self.invoice_payment_term_id.note)
            else:
                term = self.invoice_payment_term_id.name
            etree.SubElement(terms, '{%s}Note' % cbc).text = term
            if self.invoice_date_due:
                etree.SubElement(terms,
                                 '{%s}PaymentDueDate' % cbc).text = self.invoice_date_due.strftime(
                    "%Y-%m-%d")

        if self.currency_id != self.company_id.currency_id:
            if self.amount_total:
                rate = abs(self.amount_total_signed) / self.amount_total
            else:
                rate = 1 / self.currency_id.with_context(
                    date=self.invoice_date or fields.Date.context_today(self)).rate
            tax_curr = etree.SubElement(einvoice, '{%s}TaxExchangeRate' % cac)
            etree.SubElement(tax_curr,
                             '{%s}SourceCurrencyCode' % cbc).text = self.currency_id.name
            etree.SubElement(tax_curr,
                             '{%s}TargetCurrencyCode' % cbc).text = self.company_id.currency_id.name
            etree.SubElement(tax_curr,
                             '{%s}CalculationRate' % cbc).text = '%.4f' % rate
            etree.SubElement(tax_curr, '{%s}Date' % cbc).text = invoice_date
            pri_curr = etree.SubElement(einvoice,
                                        '{%s}PricingExchangeRate' % cac)
            etree.SubElement(pri_curr,
                             '{%s}SourceCurrencyCode' % cbc).text = self.currency_id.name
            etree.SubElement(pri_curr,
                             '{%s}TargetCurrencyCode' % cbc).text = self.company_id.currency_id.name
            etree.SubElement(pri_curr,
                             '{%s}CalculationRate' % cbc).text = '%.4f' % rate
            etree.SubElement(pri_curr, '{%s}Date' % cbc).text = invoice_date

        taxtotal = etree.SubElement(einvoice, '{%s}TaxTotal' % cac)
        etree.SubElement(taxtotal, '{%s}TaxAmount' % cbc,
                         attrib={
                             'currencyID': self.currency_id.name}).text = '%.*f' % (
            account_precision, self.amount_tax)

        tax_line_ids = self.line_ids.filtered(lambda line: line.tax_line_id)

        # Full Exemption
        if fp and fp.l10n_tr_fp_type == 'ISTISNA':
            taxsubtotal = etree.SubElement(taxtotal, '{%s}TaxSubtotal' % cac)
            etree.SubElement(taxsubtotal, '{%s}TaxableAmount' % cbc,
                             attrib={
                                 'currencyID': self.currency_id.name}).text = '%.*f' % (
                account_precision, self.amount_untaxed)
            etree.SubElement(taxsubtotal, '{%s}TaxAmount' % cbc,
                             attrib={
                                 'currencyID': self.currency_id.name}).text = '%.*f' % (
                account_precision, 0.0)
            taxcategory = etree.SubElement(taxsubtotal, '{%s}TaxCategory' % cac)
            etree.SubElement(taxcategory,
                             '{%s}TaxExemptionReasonCode' % cbc).text = fp.l10n_tr_fp_code
            if fp.note:
                note = self.env["ir.fields.converter"].html_to_string(fp.note)
                etree.SubElement(taxcategory,
                                 '{%s}TaxExemptionReason' % cbc).text = note
            else:
                etree.SubElement(taxcategory,
                                 '{%s}TaxExemptionReason' % cbc).text = fp.name
            taxscheme = etree.SubElement(taxcategory, '{%s}TaxScheme' % cac)
            etree.SubElement(taxscheme, '{%s}Name' % cbc).text = 'KDV'
            etree.SubElement(taxscheme, '{%s}TaxTypeCode' % cbc).text = '0015'
        elif not tax_line_ids:  # Extreme case: Exemption return
            taxsubtotal = etree.SubElement(taxtotal, '{%s}TaxSubtotal' % cac)
            etree.SubElement(taxsubtotal, '{%s}TaxableAmount' % cbc,
                             attrib={
                                 'currencyID': self.currency_id.name}).text = '%.*f' % (
                account_precision, self.amount_untaxed)
            etree.SubElement(taxsubtotal, '{%s}TaxAmount' % cbc,
                             attrib={
                                 'currencyID': self.currency_id.name}).text = '%.*f' % (
                account_precision, 0.0)
            taxcategory = etree.SubElement(taxsubtotal, '{%s}TaxCategory' % cac)
            taxscheme = etree.SubElement(taxcategory, '{%s}TaxScheme' % cac)
            etree.SubElement(taxscheme, '{%s}Name' % cbc).text = 'KDV'
            etree.SubElement(taxscheme, '{%s}TaxTypeCode' % cbc).text = '0015'
        else:
            for taxline in tax_line_ids:
                category = taxline.tax_group_id
                if (fp and fp.l10n_tr_fp_type == 'IHRACKAYITLI' and
                        category.l10n_tr_tax_type.code != "0015"):
                    continue
                if not category.l10n_tr_tax_type:
                    raise UserError(
                        _("Tax category (and its parents) has no tax type!"))
                if not category.l10n_tr_tax_type.code:
                    raise UserError(
                        _("Tax type has no code!"))
                tax_amount = abs(taxline.amount_currency)
                if category.l10n_tr_tax_type.code != "9015" and tax_amount > 0.0:
                    tax_percent = abs(taxline.tax_line_id.amount)
                    taxsubtotal = etree.SubElement(taxtotal,
                                                   '{%s}TaxSubtotal' % cac)
                    etree.SubElement(taxsubtotal, '{%s}TaxableAmount' % cbc,
                                     attrib={
                                         'currencyID': self.currency_id.name}).text = '%.*f' % (
                        account_precision, tax_amount / tax_percent * 100)
                    etree.SubElement(taxsubtotal, '{%s}TaxAmount' % cbc,
                                     attrib={
                                         'currencyID': self.currency_id.name}).text = '%.*f' % (
                        account_precision, tax_amount)
                    etree.SubElement(taxsubtotal,
                                     '{%s}CalculationSequenceNumeric' % cbc).text = str(
                        taxline.sequence)
                    if tax_percent.is_integer():
                        etree.SubElement(taxsubtotal,
                                         '{%s}Percent' % cbc).text = '%d' % tax_percent
                    else:
                        etree.SubElement(taxsubtotal,
                                         '{%s}Percent' % cbc).text = (
                                    '%f' % tax_percent).rstrip('0')
                    taxcategory = etree.SubElement(taxsubtotal,
                                                   '{%s}TaxCategory' % cac)
                    taxscheme = etree.SubElement(taxcategory,
                                                 '{%s}TaxScheme' % cac)
                    etree.SubElement(taxscheme,
                                     '{%s}Name' % cbc).text = category.l10n_tr_tax_type.name
                    etree.SubElement(taxscheme,
                                     '{%s}TaxTypeCode' % cbc).text = category.l10n_tr_tax_type.code

        # Witholding Tax
        if fp and fp.l10n_tr_fp_type == 'TEVKIFAT' and self.move_type == 'out_invoice':
            taxtotal = etree.SubElement(einvoice,
                                        '{%s}WithholdingTaxTotal' % cac)
            for taxline in tax_line_ids:
                category = taxline.tax_group_id
                if (fp and fp.l10n_tr_fp_type == 'IHRACKAYITLI' and
                        category.l10n_tr_tax_type.code != "0015"):
                    continue
                if not category.l10n_tr_tax_type:
                    raise UserError(
                        _("Tax category (and its parents) has no tax type!"))
                if not category.l10n_tr_tax_type.code:
                    raise UserError(
                        _("Tax type has no code!"))
                if category.l10n_tr_tax_type.code == "9015":
                    tax_amount = abs(taxline.amount_currency)
                    etree.SubElement(taxtotal, '{%s}TaxAmount' % cbc,
                                     attrib={
                                         'currencyID': self.currency_id.name}).text = '%.*f' % (
                        account_precision, tax_amount)
                    taxsubtotal = etree.SubElement(taxtotal,
                                                   '{%s}TaxSubtotal' % cac)
                    etree.SubElement(taxsubtotal, '{%s}TaxAmount' % cbc,
                                     attrib={
                                         'currencyID': self.currency_id.name}).text = '%.*f' % (
                        account_precision, tax_amount)
                    kdv_amount = abs(sum(tax_line_ids.filtered(
                        lambda x: x.tax_group_id.l10n_tr_tax_type.code == "0015").mapped('amount_currency')))
                    tax_percent = tax_amount / kdv_amount * 100
                    etree.SubElement(taxsubtotal,
                                     '{%s}Percent' % cbc).text = '%d' % round(
                        tax_percent)
                    taxcategory = etree.SubElement(taxsubtotal,
                                                   '{%s}TaxCategory' % cac)
                    taxscheme = etree.SubElement(taxcategory,
                                                 '{%s}TaxScheme' % cac)
                    etree.SubElement(taxscheme, '{%s}Name' % cbc).text = fp.name
                    etree.SubElement(taxscheme,
                                     '{%s}TaxTypeCode' % cbc).text = fp.l10n_tr_fp_code

        export_registered_amount = 0.0
        if fp and fp.l10n_tr_fp_type == 'IHRACKAYITLI':
            for taxline in tax_line_ids:
                if taxline.tax_group_id.l10n_tr_tax_type.code == "0015":
                    export_registered_amount += abs(taxline.amount_currency)

        line_extension_amount = 0.0
        allowance_total_amount = 0.0
        charge_total_amount = 0.0

        for line in invoice_line_ids:
            taxes = line.tax_ids.compute_all(line.price_unit,
                                                          self.currency_id,
                                                          line.quantity,
                                                          product=line.product_id,
                                                          partner=self.partner_id)
            line_extension_amount += taxes['total_excluded']
            line_price_unit = taxes['total_excluded'] / line.quantity
            if line.discount > 0:
                allowance_total_amount += line_price_unit * line.quantity * (
                            line.discount / 100)
            if line.discount < 0:
                charge_total_amount += abs(
                    line_price_unit * line.quantity * (line.discount / 100))

        legmontot = etree.SubElement(einvoice, '{%s}LegalMonetaryTotal' % cac)
        etree.SubElement(legmontot, '{%s}LineExtensionAmount' % cbc,
                         attrib={
                             'currencyID': self.currency_id.name}).text = '%.*f' % (
            account_precision, line_extension_amount)
        etree.SubElement(legmontot, '{%s}TaxExclusiveAmount' % cbc,
                         attrib={
                             'currencyID': self.currency_id.name}).text = '%.*f' % (
            account_precision, self.amount_untaxed)
        etree.SubElement(legmontot, '{%s}TaxInclusiveAmount' % cbc,
                         attrib={
                             'currencyID': self.currency_id.name}).text = '%.*f' % (
            account_precision, self.amount_total + export_registered_amount)
        etree.SubElement(legmontot, '{%s}AllowanceTotalAmount' % cbc,
                         attrib={
                             'currencyID': self.currency_id.name}).text = '%.*f' % (
            account_precision, allowance_total_amount)
        etree.SubElement(legmontot, '{%s}ChargeTotalAmount' % cbc,
                         attrib={
                             'currencyID': self.currency_id.name}).text = '%.*f' % (
            account_precision, charge_total_amount)
        etree.SubElement(legmontot, '{%s}PayableAmount' % cbc,
                         attrib={
                             'currencyID': self.currency_id.name}).text = '%.*f' % (
            account_precision, self.amount_total)

        line_seq = 0
        for line in invoice_line_ids:
            line_seq += 1
            currency = line.currency_id

            taxes = line.tax_ids.compute_all(line.price_unit, currency,
                                             line.quantity,
                                             product=line.product_id,
                                             partner=line.move_id.partner_id)

            line_extension_amount += taxes['total_excluded']
            line_price_unit = taxes['total_excluded'] / line.quantity

            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(price, currency, line.quantity,
                                             product=line.product_id,
                                             partner=line.move_id.partner_id)

            invoiceline = etree.SubElement(einvoice, '{%s}InvoiceLine' % cac)
            etree.SubElement(invoiceline, '{%s}ID' % cbc).text = str(line_seq)
            if line.product_id:
                self.einvoice_generate_invoice_line_note_xml(invoiceline, cac, cbc, line)

            # etree.SubElement(invoiceline, '{%s}Note' % cbc).text = line.name
            if not line.product_uom_id:
                raise UserError(_("Unit of measure is needed on invoice line!"))
            if not line.product_uom_id.unece_code:
                raise UserError(_(
                    "Unit of measure code is missing! It has to be a valid UNECE code!"))
            etree.SubElement(invoiceline, '{%s}InvoicedQuantity' % cbc,
                             attrib={
                                 'unitCode': line.product_uom_id.unece_code}).text = '%.*f' % (
            uom_precision, line.quantity)
            etree.SubElement(invoiceline, '{%s}LineExtensionAmount' % cbc,
                             attrib={
                                 'currencyID': self.currency_id.name}).text = \
                '%.*f' % (account_precision, (price * line.quantity))

            self.einvoice_generate_delivery_line_xml(invoiceline, line,
                                                     price_precision,
                                                     line_price_unit,
                                                     cac, cbc)

            if line.discount != 0:
                allowance = etree.SubElement(invoiceline,
                                             '{%s}AllowanceCharge' % cac)
                if line.discount > 0:
                    etree.SubElement(allowance,
                                     '{%s}ChargeIndicator' % cbc).text = 'false'
                else:
                    etree.SubElement(allowance,
                                     '{%s}ChargeIndicator' % cbc).text = 'true'
                etree.SubElement(allowance,
                                 '{%s}MultiplierFactorNumeric' % cbc).text = '%.*f' % (
                    discount_precision + 2, abs(line.discount) / 100)
                etree.SubElement(allowance, '{%s}Amount' % cbc,
                                 attrib={
                                     'currencyID': self.currency_id.name}).text = \
                    '%.*f' % (account_precision, abs(
                        line_price_unit * line.quantity * (
                                    line.discount / 100)))
                etree.SubElement(allowance, '{%s}BaseAmount' % cbc,
                                 attrib={
                                     'currencyID': self.currency_id.name}).text = '%.*f' % (
                    price_precision, line_price_unit)

            taxtotal = etree.SubElement(invoiceline, '{%s}TaxTotal' % cac)

            price_tax = line.price_total - line.price_subtotal

            etree.SubElement(taxtotal, '{%s}TaxAmount' % cbc,
                             attrib={
                                 'currencyID': self.currency_id.name}).text = '%.*f' % (
                account_precision, price_tax)

            # hardcode 0 tax if there is no tax
            if len(taxes['taxes']) == 0:
                if self.move_type != 'in_refund' and \
                        (not fp or fp.l10n_tr_fp_type != 'ISTISNA'):
                    raise UserError(_(
                        "Invoice line must have tax unless it's fiscal position category is exception!"))
                taxsubtotal = etree.SubElement(taxtotal,
                                               '{%s}TaxSubtotal' % cac)
                etree.SubElement(taxsubtotal, '{%s}TaxableAmount' % cbc,
                                 attrib={
                                     'currencyID': self.currency_id.name}).text = \
                    '%.*f' % (account_precision, abs(
                        line_price_unit * line.quantity * (
                                    line.discount / 100)))
                etree.SubElement(taxsubtotal, '{%s}TaxAmount' % cbc,
                                 attrib={
                                     'currencyID': self.currency_id.name}).text = '%.*f' % (
                    account_precision, 0.0)

                etree.SubElement(taxsubtotal,
                                 '{%s}CalculationSequenceNumeric' % cbc).text = '1'
                etree.SubElement(taxsubtotal, '{%s}Percent' % cbc).text = '0'
                taxcategory = etree.SubElement(taxsubtotal,
                                               '{%s}TaxCategory' % cac)
                taxscheme = etree.SubElement(taxcategory, '{%s}TaxScheme' % cac)
                etree.SubElement(taxscheme, '{%s}Name' % cbc).text = 'KDV'
                etree.SubElement(taxscheme,
                                 '{%s}TaxTypeCode' % cbc).text = '0015'

            for taxline in taxes['taxes']:
                tax = self.env['account.tax'].browse(taxline['id'])
                category = tax.tax_group_id
                if (fp and fp.l10n_tr_fp_type == 'IHRACKAYITLI' and
                        category.l10n_tr_tax_type.code != "0015"):
                    continue
                if not category.l10n_tr_tax_type:
                    raise UserError(
                        _("Tax category (and its parents) has no tax type!"))
                if not category.l10n_tr_tax_type.code:
                    raise UserError(
                        _("Tax type has no code!"))
                if category.l10n_tr_tax_type.code != "9015":
                    taxsubtotal = etree.SubElement(taxtotal,
                                                   '{%s}TaxSubtotal' % cac)
                    etree.SubElement(taxsubtotal, '{%s}TaxableAmount' % cbc,
                                     attrib={
                                         'currencyID': self.currency_id.name}).text = '%.*f' % (
                        account_precision, line.price_subtotal)
                    etree.SubElement(taxsubtotal, '{%s}TaxAmount' % cbc,
                                     attrib={
                                         'currencyID': self.currency_id.name}).text = '%.*f' % (
                        account_precision, taxline['amount'])
                    etree.SubElement(taxsubtotal,
                                     '{%s}CalculationSequenceNumeric' % cbc).text = \
                        str(taxline['sequence'])
                    tax_percent = abs(tax.amount)
                    if tax_percent.is_integer():
                        etree.SubElement(taxsubtotal,
                                         '{%s}Percent' % cbc).text = '%d' % tax_percent
                    else:
                        etree.SubElement(taxsubtotal,
                                         '{%s}Percent' % cbc).text = (
                                    '%f' % tax_percent).rstrip('0')
                    taxcategory = etree.SubElement(taxsubtotal,
                                                   '{%s}TaxCategory' % cac)
                    taxscheme = etree.SubElement(taxcategory,
                                                 '{%s}TaxScheme' % cac)
                    etree.SubElement(taxscheme,
                                     '{%s}Name' % cbc).text = category.l10n_tr_tax_type.name
                    etree.SubElement(taxscheme,
                                     '{%s}TaxTypeCode' % cbc).text = category.l10n_tr_tax_type.code

            item = etree.SubElement(invoiceline, '{%s}Item' % cac)
            if not line.name:
                raise UserError(_(
                    'Description is missing! All invoice lines must have a description.'))
            etree.SubElement(item, '{%s}Name' % cbc).text = line.name
            if line.product_id:
                self.einvoice_generate_product_xml(item, cac, cbc, line)

            price = etree.SubElement(invoiceline, '{%s}Price' % cac)
            etree.SubElement(price, '{%s}PriceAmount' % cbc,
                             attrib={
                                 'currencyID': self.currency_id.name}).text = '%.*f' % (
                price_precision, line_price_unit)

        schema_file = file_open(
            'l10n_tr_edi/data/xsd/maindoc/UBL-Invoice-2.1-int.xsd')
        xmlschema_doc = etree.parse(schema_file)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        try:
            xmlschema.assertValid(einvoice)
        except DocumentInvalid as e:
            raise UserError(
                _("E-Invoice xsd validation failed!") + '\n\n' + e.args[0])
        return einvoice

    @api.model
    def einvoice_generate_response_ubl_xml_etree(self,
                                                 response_type='accepted'):
        l10n_tr_einvoice_uuid = str(uuid.uuid4())
        xmlns = 'urn:oasis:names:specification:ubl:schema:xsd:ApplicationResponse-2'
        cac = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
        cbc = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
        ext = 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2'
        einvoice = etree.Element('{%s}ApplicationResponse' % xmlns,
                                 nsmap={
                                     None: xmlns,
                                     'cac': cac,
                                     'cbc': cbc,
                                     'ext': ext
                                 })
        etree.SubElement(einvoice, '{%s}UBLVersionID' % cbc).text = '2.1'
        etree.SubElement(einvoice, '{%s}CustomizationID' % cbc).text = 'TR1.2'
        etree.SubElement(einvoice,
                         '{%s}ProfileID' % cbc).text = self.l10n_tr_einvoice_profile
        etree.SubElement(einvoice, '{%s}ID' % cbc).text = self.l10n_tr_document_number
        etree.SubElement(einvoice, '{%s}UUID' % cbc).text = l10n_tr_einvoice_uuid
        now = datetime.now(pytz.timezone('Europe/Istanbul'))
        etree.SubElement(einvoice, '{%s}IssueDate' % cbc).text = now.strftime(
            "%Y-%m-%d")
        etree.SubElement(einvoice, '{%s}IssueTime' % cbc).text = now.strftime(
            "%H:%M:%S")

        if self.move_type == 'out_invoice':
            accounting_party = 'company'
        else:
            accounting_party = 'partner'

        commercial_partner = self.partner_id.commercial_partner_id

        self.company_id.partner_id.ubltr_generate_party_xml(
            'sender', einvoice, cac, cbc,
            commercial_partner.l10n_tr_party_identifiers, accounting_party)

        commercial_partner.ubltr_generate_party_xml(
            'receiver', einvoice, cac, cbc,
            commercial_partner.l10n_tr_party_identifiers, accounting_party)

        if response_type == 'accepted':
            response_code = 'KABUL'
            response_desc = _('Invoice Accepted')
        else:
            response_code = 'RED'
            response_desc = _('Invoice Rejected')

        doc_resp = etree.SubElement(einvoice, '{%s}DocumentResponse' % cac)
        response = etree.SubElement(doc_resp, '{%s}Response' % cac)
        etree.SubElement(response, '{%s}ReferenceID' % cbc).text = '12345678910'
        etree.SubElement(response,
                         '{%s}ResponseCode' % cbc).text = response_code
        etree.SubElement(response, '{%s}Description' % cbc).text = response_desc

        doc_ref = etree.SubElement(doc_resp, '{%s}DocumentReference' % cac)
        etree.SubElement(doc_ref, '{%s}ID' % cbc).text = self.l10n_tr_einvoice_uuid
        etree.SubElement(doc_ref,
                         '{%s}IssueDate' % cbc).text = self.invoice_date.strftime(
            "%Y-%m-%d")
        etree.SubElement(doc_ref, '{%s}DocumentTypeCode' % cbc).text = 'FATURA'
        etree.SubElement(doc_ref, '{%s}DocumentType' % cbc).text = 'FATURA'

        line_response = etree.SubElement(doc_resp, '{%s}LineResponse' % cac)
        line_reference = etree.SubElement(line_response,
                                          '{%s}LineReference' % cac)
        etree.SubElement(line_reference, '{%s}LineID' % cbc)
        response2 = etree.SubElement(line_response, '{%s}Response' % cac)
        etree.SubElement(response2,
                         '{%s}ReferenceID' % cbc).text = '12345678911'
        etree.SubElement(response2,
                         '{%s}ResponseCode' % cbc).text = response_code
        etree.SubElement(response2,
                         '{%s}Description' % cbc).text = response_desc

        schema_file = file_open(
            'l10n_tr_edi/data/xsd/maindoc/UBL-ApplicationResponse-2.1.xsd')
        xmlschema_doc = etree.parse(schema_file)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        try:
            xmlschema.assertValid(einvoice)
        except DocumentInvalid as e:
            raise UserError(
                _("E-Invoice xsd validation failed!") + '\n\n' + e.args[0])

        return einvoice

    @api.model
    def einvoice_generate_ubl_xml_string(self, pretty_print=False):
        xml_tree = self.einvoice_generate_ubl_xml_etree()
        return etree.tostring(xml_tree,
                              encoding='utf-8',
                              method='xml',
                              pretty_print=pretty_print,
                              xml_declaration=False)

    # actions
    def action_einvoice_get_status(self):
        for invoice in self:
            invoice.einvoice_get_status()

    @api.model
    def einvoice_response_period_expired(self):
        last_date = self.create_date + relativedelta(days=7)
        last = last_date.replace(tzinfo=pytz.utc).astimezone(
            pytz.timezone('Europe/Istanbul'))
        today = datetime.now(pytz.timezone('Europe/Istanbul'))
        return last.date() < today.date()

    def action_einvoice_accept(self):
        for invoice in self:
            if invoice.einvoice_response_period_expired():
                invoice.action_einvoice_completed(_('E-invoice accepted'))
            else:
                invoice.l10n_tr_einvoice_response_type = 'accepted'
                invoice.einvoice_send_response()

    def action_einvoice_reject(self):
        for invoice in self:
            if invoice.einvoice_response_period_expired():
                raise UserError(_("Invoices cannot be rejected after 7 days!"))
            else:
                invoice.l10n_tr_einvoice_response_type = 'rejected'
                invoice.einvoice_send_response()

    def action_einvoice_resend(self):
        for inv in self:
            if inv.move_type in ['out_invoice', 'in_refund'] and \
                    inv.l10n_tr_delivery_type == 'einvoice':
                inv.l10n_tr_einvoice_uuid = False
                inv.l10n_tr_einvoice_envelope_uuid = False
                inv.einvoice_send()

    # callbacks
    @api.model
    def action_einvoice_sent(self, message):
        if self.l10n_tr_einvoice_state != 'sent':
            self.write({'l10n_tr_einvoice_state': 'sent'})
            self.message_post(body=message)

    @api.model
    def action_einvoice_waiting(self, message):
        if self.l10n_tr_einvoice_state != 'waiting':
            self.write({'l10n_tr_einvoice_state': 'waiting'})
            self.message_post(body=message)

    @api.model
    def action_einvoice_completed(self, message):
        if self.l10n_tr_einvoice_state != 'completed':
            self.write({'l10n_tr_einvoice_state': 'completed'})
            self.message_post(body=message)

    @api.model
    def action_einvoice_failed(self, message):
        if self.l10n_tr_einvoice_state != 'failed':
            self.write({'l10n_tr_einvoice_state': 'failed'})
            self.message_post(body=message)

    @api.model
    def action_einvoice_accepted(self, message):
        if self.l10n_tr_einvoice_state != 'completed':
            self.write({'l10n_tr_einvoice_state': 'completed'})
            self.message_post(body=message)

    @api.model
    def action_einvoice_rejected(self, message):
        if self.l10n_tr_einvoice_state != 'rejected':
            self.write({'l10n_tr_einvoice_state': 'rejected'})
            self.message_post(body=message)

    # report_xslt hook methods
    @api.model
    def _get_xml_etree(self):
        return self.einvoice_generate_ubl_xml_etree()

    # Send E-Invoice
    @api.model
    def einvoice_send(self):
        if not self.l10n_tr_einvoice_envelope_uuid:
            self.l10n_tr_einvoice_envelope_uuid = str(uuid.uuid4())
        xml_tree = self.einvoice_generate_ubl_xml_etree()
        data = self.company_id.ubltr_generate_envelope_xml(
            self.l10n_tr_einvoice_envelope_uuid,
            'SENDERENVELOPE',
            self.l10n_tr_einvoice_sender_id,
            self.l10n_tr_einvoice_postbox_id,
            'INVOICE',
            xml_tree)
        output = io.BytesIO()
        file = zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED)
        file.writestr('%s.xml' % self.l10n_tr_einvoice_envelope_uuid, data)
        file.close()
        bytedata = base64.encodebytes(output.getvalue())
        params = self.company_id.einvoice_get_connect_params()
        params.update({
            'envelope': bytedata.decode(),
        })
        endpoint = self.company_id._get_default_endpoint()
        _logger.info("einvoice_send %s" % self.l10n_tr_einvoice_sender_id.name)
        iap_jsonrpc(endpoint + '/efatura/1/send_ubl', params=params, timeout=120)
        self.action_einvoice_sent(_('E-Invoice sent'))
        # attach pdf
        self.einvoice_attach_pdf(xml_tree)

    # Send E-Archive Invoice
    @api.model
    def earchive_send(self):
        xml_tree = self.einvoice_generate_ubl_xml_etree()
        # add unecessary but mandatory nodes
        cac = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
        cbc = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
        ext = 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2'
        extensions = etree.Element('{%s}UBLExtensions' % ext)
        extension = etree.SubElement(extensions, '{%s}UBLExtension' % ext)
        etree.SubElement(extension, '{%s}ExtensionContent' % ext).text = " "
        xml_tree.insert(0, extensions)
        supplier = xml_tree.find(".//{%s}AccountingSupplierParty" % cac)
        signature = etree.Element('{%s}Signature' % cac)
        etree.SubElement(signature, '{%s}ID' % cbc,
                         attrib={'schemeID': 'VKN_TCKN'}).text = '1111111111'
        self.company_id.partner_id.ubltr_generate_party_xml('signatory',
                                                            signature, cac, cbc)
        dsa = etree.SubElement(signature,
                               '{%s}DigitalSignatureAttachment' % cac)
        er = etree.SubElement(dsa, '{%s}ExternalReference' % cac)
        etree.SubElement(er, '{%s}URI' % cbc).text = '#Signature'
        xml_tree.insert(xml_tree.index(supplier), signature)

        data = etree.tostring(xml_tree, encoding='utf-8', method='xml')
        output = io.BytesIO()
        file = zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED)
        file.writestr('%s.xml' % self.l10n_tr_einvoice_uuid, data)
        file.close()
        hash = md5(output.getvalue()).hexdigest()
        bytedata = base64.encodebytes(output.getvalue())
        params = self.company_id.einvoice_get_connect_params()
        params.update({
            'invoice': bytedata.decode(),
            'hash': hash,
        })
        endpoint = self.company_id._get_default_endpoint()
        _logger.info("earchive_send %s" % self.l10n_tr_document_number)
        iap_jsonrpc(endpoint + '/earsiv/1/send_invoice', params=params, timeout=120)
        self.action_einvoice_completed(_('E-Archive invoice completed'))
        if self.company_id.l10n_tr_earchive_auto_email:
            template_id = self.env.ref(self._get_mail_template(), raise_if_not_found=False)
            self.with_context(force_send=True).message_post_with_template(
                template_id.id, email_layout_xmlid='mail.mail_notification_light')
        else:
            # attach pdf
            self.einvoice_attach_pdf(xml_tree)

    # E-Arşiv Fatura İptal Et
    @api.model
    def earchive_cancel(self):
        invoice_number = self.l10n_tr_document_number
        invoice_amount = self.amount_untaxed
        invoice_date = self.invoice_date.strftime("%Y-%m-%d")
        params = self.company_id.einvoice_get_connect_params()
        params.update({
            'invoice': invoice_number,
            'amount': invoice_amount,
            'date': invoice_date,
        })
        _logger.info("earchive_cancel %s" % invoice_number)
        endpoint = self.company_id._get_default_endpoint()
        iap_jsonrpc(endpoint + '/earsiv/1/cancel_invoice', params=params,
                timeout=120)

    # Query Invoice Status
    def einvoice_get_status(self):
        account = self.env['iap.account'].get_company_account('efatura', self[0].company_id)
        tax_number = self[0].company_id.partner_id.ubltr_get_vat()
        db_uuid = self.env['ir.config_parameter'].sudo().get_param(
            'database.uuid')
        params = {
            'db_uuid': db_uuid,
            'account_token': account.account_token,
            'tax_number': tax_number
        }

        # group by 20
        def chunker(seq, size):
            return (seq[pos:pos + size] for pos in range(0, len(seq), size))

        for group in chunker(self, 20):
            if group[0].move_type in ('out_invoice', 'in_refund'):
                identifier = group[0].l10n_tr_einvoice_sender_id.name
                uuids = group.mapped('l10n_tr_einvoice_envelope_uuid')
            else:
                identifier = group[0].l10n_tr_einvoice_postbox_id.name
                uuids = group.mapped('l10n_tr_einvoice_response_uuid')
            params['identifier'] = identifier
            params['envelope_uuids'] = uuids
            endpoint = self[0].company_id._get_default_endpoint()
            _logger.info("einvoice_get_status %s" % identifier)
            status_list = iap_jsonrpc(endpoint + '/efatura/1/get_envelope_status',
                                  params=params, timeout=120)
            for status in status_list:
                if status['response_code'] == '1300':
                    for invoice in group:
                        if invoice.l10n_tr_einvoice_envelope_uuid == status[
                            'envelope_uuid']:
                            if invoice.l10n_tr_einvoice_profile == 'TICARIFATURA':
                                invoice.action_einvoice_waiting(
                                    _('E-Invoice transmitted'))
                            else:
                                invoice.action_einvoice_completed(
                                    _('E-Invoice transmitted'))
                        elif invoice.l10n_tr_einvoice_response_uuid == status[
                            'envelope_uuid']:
                            if invoice.l10n_tr_einvoice_profile == 'TICARIFATURA':
                                if invoice.l10n_tr_einvoice_response_type == 'accepted':
                                    invoice.action_einvoice_accepted(
                                        _('E-Invoice response transmitted'))
                                else:
                                    invoice.action_einvoice_rejected(
                                        _('E-Invoice response transmitted'))
                elif status['response_code'] not in ['1000', '1100', '1200',
                                                     '1210', '1220']:
                    for invoice in group:
                        if invoice.l10n_tr_einvoice_envelope_uuid == status[
                            'envelope_uuid'] or \
                                invoice.l10n_tr_einvoice_response_uuid == status[
                            'envelope_uuid']:
                            invoice.action_einvoice_failed(
                                status['description'])

    # Send Response
    @api.model
    def einvoice_send_response(self):
        for invoice in self:
            invoice.l10n_tr_einvoice_response_uuid = str(uuid.uuid4())
            response_type = invoice.l10n_tr_einvoice_response_type
            xml_tree = invoice.einvoice_generate_response_ubl_xml_etree(
                response_type)
            data = self.company_id.ubltr_generate_envelope_xml(
                invoice.l10n_tr_einvoice_response_uuid,
                'POSTBOXENVELOPE',
                invoice.l10n_tr_einvoice_postbox_id,
                invoice.l10n_tr_einvoice_sender_id,
                'APPLICATIONRESPONSE',
                xml_tree)
            output = io.BytesIO()
            file = zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED)
            file.writestr('%s.xml' % invoice.l10n_tr_einvoice_response_uuid, data)
            file.close()
            bytedata = base64.encodebytes(output.getvalue())
            params = self.company_id.einvoice_get_connect_params()
            params.update({
                'envelope': bytedata.decode(),
            })
            endpoint = self.company_id._get_default_endpoint()
            _logger.info("einvoice_send_response%s" % self.l10n_tr_document_number)
            iap_jsonrpc(endpoint + '/efatura/1/send_ubl', params=params,
                    timeout=120)
            if response_type == 'accepted':
                invoice.action_einvoice_sent(
                    _('E-Invoice response sent (accepted)'))
            else:
                invoice.action_einvoice_sent(
                    _('E-Invoice response sent (rejected)'))
