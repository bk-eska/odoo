# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import io
import zipfile
import base64
from dateutil import tz
import pytz
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from lxml import etree
from lxml.etree import DocumentInvalid

import logging
_logger = logging.getLogger(__name__)

from odoo import _, api, models, fields
from odoo.addons.iap.tools.iap_tools import iap_jsonrpc
from odoo.exceptions import UserError
from odoo.tools.misc import file_open
from odoo.tools import pycompat


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_tr_einvoice_enabled = fields.Boolean(
        string='E-Invoice Enabled',
    )

    l10n_tr_einvoice_sender_ids = fields.One2many(
        comodel_name='l10n_tr.einvoice.sender',
        inverse_name='company_id',
        string='E-Invoice Senders',
        help='E-Invoice Senders for this company.',
    )

    l10n_tr_einvoice_postbox_ids = fields.One2many(
        comodel_name='l10n_tr.einvoice.postbox',
        inverse_name='company_id',
        string='E-Invoice Postboxes',
        help='E-Invoice Postboxes for this company.',
    )

    l10n_tr_einvoice_user_download = fields.Boolean(
        string='Download Registered User List',
    )

    l10n_tr_einvoice_user_download_sequence = fields.Integer(
        string='E-Invoice Registered User Download Sequence',
        default=1,
    )

    l10n_tr_einvoice_user_download_date = fields.Date(
        string="E-Invoice Registered User Download Date",
    )

    l10n_tr_einvoice_import_invoice_lines = fields.Boolean(
        string='Import Incoming Invoice Lines',
    )

    l10n_tr_earchive_auto_email = fields.Boolean(
        string='E-Archive Auto E-Mail',
    )

    @api.model
    def run_get_registered_users(self):
        company = self.search([
            ('l10n_tr_einvoice_user_download', '=', True)
        ], limit=1)
        if company:
            company.einvoice_get_registered_users()

    @api.model
    def run_get_einvoices(self):
        for company in self.search([('l10n_tr_einvoice_enabled', '=', True)]):
            company.with_context(lang='tr_TR').l10n_tr_einvoice_postbox_ids.get_invoices()

    @api.model
    def run_get_responses(self):
        for company in self.search([('l10n_tr_einvoice_enabled', '=', True)]):
            company.with_context(lang='tr_TR').l10n_tr_einvoice_sender_ids.get_responses()

    @api.model
    def run_update_einvoices(self):
        for company in self.search([('l10n_tr_einvoice_enabled', '=', True)]):
            company.l10n_tr_einvoice_sender_ids.update_invoices()
            company.l10n_tr_einvoice_postbox_ids.update_invoices()

    @api.model
    def einvoice_process_invoice_lines(self, einvoice, ns, invoice,
                                       partner_id, invoice_type):

        self._cr.execute('SAVEPOINT invoice_lines_create')

        try:
            lines = einvoice.xpath('./cac:InvoiceLine', namespaces=ns)
            for line in lines:
                seq = self.ubltr_get_field(line, ns, './cbc:ID')
                iq = line.xpath('./cbc:InvoicedQuantity', namespaces=ns)[0]
                qty = float(iq.text)
                uom_code = iq.get("unitCode")
                uom_id = self.env['uom.uom'].search([
                    ('unece_code', '=', uom_code)], limit=1)
                uom = uom_id and uom_id.id or False
                upc = float(self.ubltr_get_field(
                    line, ns, './cac:Price/cbc:PriceAmount'))

                name = self.ubltr_get_field(
                    line, ns, './cac:Item/cbc:Name')
                desc = self.ubltr_get_field(
                    line, ns, './cac:Item/cbc:Description')
                if desc:
                    name = name + ' ' + desc

                product_id = self.ubltr_find_product(self,
                    line, ns, partner_id,
                    invoice_type == 'in_refund',
                    invoice_type == 'in_invoice')
                product = product_id and product_id.id or False

                journal = invoice.journal_id

                inv_line = {
                    'invoice_id': invoice.id,
                    'quantity': qty,
                    'sequence': seq,
                    'account_id': journal.payment_credit_account_id.id
                }

                if product:
                    inv_line['product_id'] = product

                if uom:
                    inv_line['product_uom_id'] = uom
                inv_line['name'] = name
                inv_line['price_unit'] = upc

                alws = line.xpath('./cac:AllowanceCharge', namespaces=ns)
                total_discount = 0.0
                for alw in alws:
                    ind = self.ubltr_get_field(
                        alw, ns, './cbc:ChargeIndicator')
                    disc_amt = float(self.ubltr_get_field(
                        alw, ns, './cbc:Amount'))
                    if ind == 'true':
                        disc_amt *= -1
                    total_discount += disc_amt
                if total_discount != 0:
                    discount = total_discount / (upc * qty) * 100
                    inv_line['discount'] = discount

                line = self.env['account.move.line'].\
                    with_context({}).create(inv_line)
                line._set_taxes()

        except Exception:
            # if something happens rollback line inserts
            self._cr.execute('ROLLBACK TO SAVEPOINT invoice_lines_create')
            pass

    @api.model
    def einvoice_process_invoice(self, ubl, sender, postbox, envelope_uuid):

        _logger.info("einvoice_process_invoice %s %s %s" %
                     (sender, postbox, envelope_uuid))
        ns = {
            'cac': "urn:oasis:names:specification:ubl:schema:xsd:"
                   "CommonAggregateComponents-2",
            'cbc': "urn:oasis:names:specification:ubl:schema:xsd:"
                   "CommonBasicComponents-2",
        }

        parser = etree.XMLParser(recover=True)
        einvoice = etree.fromstring(ubl, parser)

        schema_file = file_open('l10n_tr_edi/data/xsd/maindoc/'
                                'UBL-Invoice-2.1.xsd')
        xmlschema_doc = etree.parse(schema_file)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        try:
            xmlschema.assertValid(einvoice)
        except DocumentInvalid as e:
            _logger.error("E-Invoice xsd validation failed!" + '\n\n' + e.args[0])
            pass

        invtypecode = self.ubltr_get_field(einvoice, ns, './cbc:InvoiceTypeCode')
        if invtypecode not in ['IADE', 'TEVKIFATIADE']:
            journal_type = 'purchase'
            invoice_type = 'in_invoice'
        else:
            journal_type = 'sale'
            invoice_type = 'out_refund'

        number = self.ubltr_get_field(einvoice, ns, './cbc:ID')
        date = self.ubltr_get_field(einvoice, ns, './cbc:IssueDate')
        profile = self.ubltr_get_field(einvoice, ns, './cbc:ProfileID')
        uuid = self.ubltr_get_field(einvoice, ns, './cbc:UUID')
        partner_id = self.ubltr_find_partner(einvoice, ns,
                                             'AccountingSupplierParty')

        if self.env['account.move'].search([
            ('partner_id', '=', partner_id.id),
            ('l10n_tr_document_number', '=', number),
        ], limit=1):
            return

        curr = self.ubltr_get_field(einvoice, ns, './cbc:DocumentCurrencyCode')
        currency_id = self.env['res.currency'].search([
            ('name', '=', curr)], limit=1)
        if not currency_id:
            currency_id = self.env['res.currency'].search(
                [('name', '=', 'TRY')], limit=1)

        journal_id = self.env['account.journal'].search([
            ('type', '=', journal_type),
            ('company_id', '=', self.id)
        ], limit=1)

        inv = {
            'l10n_tr_document_number': number,
            'journal_id': journal_id.id or False,
            'move_type': invoice_type,
            'partner_id': partner_id.id,
            'currency_id': currency_id.id,
            'company_id': self.id,
            'invoice_date': date,
            'date': date,
            'l10n_tr_delivery_type': 'einvoice',
            'l10n_tr_einvoice_profile': profile,
            'l10n_tr_einvoice_uuid': uuid,
            'l10n_tr_einvoice_envelope_uuid': envelope_uuid,
        }

        if sender:
            sender_id = self.env['l10n_tr.einvoice.sender'].search([
                ('partner_id', '=', partner_id.id),
                ('name', '=', sender),
            ], limit=1)
            if not sender_id:
                sender_id = self.env['l10n_tr.einvoice.sender'].\
                    with_context({}).create({
                    'partner_id': partner_id.id,
                    'name': sender,
                })
            inv['l10n_tr_einvoice_sender_id'] = sender_id.id

        if postbox:
            postbox_id = self.env['l10n_tr.einvoice.postbox'].search([
                ('company_id', '=', self.id),
                ('name', '=', postbox),
            ], limit=1)
            if postbox_id:
                inv['l10n_tr_einvoice_postbox_id'] = postbox_id.id
                if postbox_id.journal_id  and invoice_type == 'in_invoice':
                    inv['journal_id'] = postbox_id.journal_id.id

        narration = ''
        notes = einvoice.xpath('./cbc:Note', namespaces=ns)
        for note in notes:
            if note.text:
                narration += note.text
                narration += '\n'

        if narration:
            inv['narration'] = narration

        if invtypecode in ['IADE', 'TEVKIFATIADE']:
            reference = self.ubltr_get_field(
                einvoice, ns, "./cac:BillingReference/"
                              "cac:InvoiceDocumentReference/"
                              "cbc:DocumentTypeCode[.='FATURA']/../cbc:ID")
            # gib örneklerinin birisinde yukarıdaki diğerinde aşağıdaki var.
            # her ikisini de destekliyoruz
            if not reference:
                reference = self.ubltr_get_field(
                    einvoice, ns, "./cac:AdditionalDocumentReference/"
                                  "cbc:DocumentTypeCode[.='IADE']/../cbc:ID")
            if reference:
                inv['ref'] = reference

        fiscal_position = False

        # Exemption
        exemption_code = self.ubltr_get_field(
            einvoice, ns, "./cac:TaxTotal/cac:TaxSubtotal/"
                          "cac:TaxCategory/cbc:TaxExemptionReasonCode")

        if exemption_code:
            if exemption_code == '311':
                inv['l10n_tr_document_type'] = 'shipment'
            fiscal_position = self.env['account.fiscal.position'].search([
                ('l10n_tr_fp_code', '=', exemption_code),
                ('company_id', '=', self.id), ], limit=1)

        # Witholding
        withholding_code = self.ubltr_get_field(
            einvoice, ns, "./cac:WithholdingTaxTotal/cac:TaxSubtotal/"
                          "cac:TaxCategory/cac:TaxScheme/cbc:TaxTypeCode")
        if withholding_code:
            fiscal_position = self.env['account.fiscal.position'].search([
                ('l10n_tr_fp_code', '=', withholding_code),
                ('company_id', '=', self.id), ], limit=1)

        if fiscal_position:
            inv['fiscal_position_id'] = fiscal_position.id

        due_date = self.ubltr_get_field(
            einvoice, ns, "./cac:PaymentMeans/cbc:PaymentDueDate")
        if due_date and due_date > '2015-01-01':
            inv['invoice_date_due'] = due_date

        invoice = self.env['account.move'].with_context({}).create(inv)

        if self.l10n_tr_einvoice_import_invoice_lines \
                or partner_id.l10n_tr_einvoice_import_invoice_lines:
            self.einvoice_process_invoice_lines(
                einvoice, ns, invoice, partner_id, invoice_type)

        if profile == 'TICARIFATURA':
            invoice.action_einvoice_waiting(_('E-Invoice waiting response'))
        else:
            invoice.action_einvoice_completed(_('E-Invoice received'))

        try:
            xslt = self.ubltr_get_field(
                einvoice, ns, "./cac:AdditionalDocumentReference/"
                              "cbc:DocumentType[translate"
                              "(.,'xslt','XSLT') = 'XSLT']/"
                              "../cac:Attachment/"
                              "cbc:EmbeddedDocumentBinaryObject")
            if not xslt:
                xslt = self.ubltr_get_field(
                    einvoice, ns, "./cac:AdditionalDocumentReference/"
                                  "cac:Attachment/"
                                  "cbc:EmbeddedDocumentBinaryObject[contains"
                                  "(translate(@filename,'xslt','XSLT'),'XSLT')]")
            if xslt:
                xslt_etree = etree.fromstring(base64.b64decode(xslt))
                invoice.einvoice_attach_pdf(einvoice, xslt_etree)
        except Exception:
            pass

    @api.model
    def einvoice_process_response(self, envelope_uuid, document, invoice, response, ns):
        response_code = self.ubltr_get_field(
            response, ns, './cac:Response/cbc:ResponseCode')
        description = self.ubltr_get_field(
            response, ns, './cac:Response/cbc:Description')
        if response_code in ['KABUL', 'IADE']:
            invoice.l10n_tr_einvoice_response_uuid = envelope_uuid
            invoice.action_einvoice_accepted(description)
        elif response_code == 'RED':
            invoice.l10n_tr_einvoice_response_uuid = envelope_uuid
            invoice.action_einvoice_rejected(description)

    @api.model
    def einvoice_process_response_document(self, ubl, document_type, envelope_uuid):

        _logger.info("einvoice_process_response_document %s %s" %
                     (document_type, envelope_uuid))

        ns = {
            'cac': "urn:oasis:names:specification:ubl:schema:xsd:"
                   "CommonAggregateComponents-2",
            'cbc': "urn:oasis:names:specification:ubl:schema:xsd:"
                   "CommonBasicComponents-2",
        }

        parser = etree.XMLParser(recover=True)
        document = etree.fromstring(ubl, parser)

        schema_file = file_open('l10n_tr_edi/data/xsd/maindoc/'
                                'UBL-ApplicationResponse-2.1.xsd')
        xmlschema_doc = etree.parse(schema_file)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        try:
            xmlschema.assertValid(document)
        except DocumentInvalid as e:
            _logger.error("E-Invoice response xsd validation failed!\n" + e.args[0])
            pass

        responses = document.xpath('//cac:DocumentResponse', namespaces=ns)
        for response in responses:
            uuid = self.ubltr_get_field(
                response, ns, './cac:DocumentReference/cbc:ID')
            if not uuid:
                return
            invoice = self.env['account.move'].search([
                ('l10n_tr_einvoice_uuid', '=', uuid)], limit=1)
            if not invoice:
                _logger.error("E-Invoice not found! UUID=" + uuid + ' ' +
                              'Envelope UUID=' + envelope_uuid)
            elif document_type != 'POSTBOXENVELOPE':
                _logger.error("Not Postbox Envelope! UUID=" + uuid + ' '+
                              'Envelope UUID=' + envelope_uuid)
            else:
                self.einvoice_process_response(envelope_uuid, document,
                                               invoice, response, ns)


    @api.model
    def einvoice_process_envelope(self, envelope):
        ns = {
            'sh': "http://www.unece.org/cefact/namespaces/"
                  "StandardBusinessDocumentHeader",
            'ef': "http://www.efatura.gov.tr/package-namespace",
            'xsi': "http://www.w3.org/2001/XMLSchema-instance",
        }

        parser = etree.XMLParser(recover=True)
        env = etree.fromstring(envelope, parser)
        uuid = self.ubltr_get_field(
            env, ns, '//sh:DocumentIdentification/sh:InstanceIdentifier')
        document_type = self.ubltr_get_field(
            env, ns, '//sh:DocumentIdentification/sh:Type')
        sender = self.ubltr_get_field(
            env, ns, '//sh:Sender/sh:Identifier')
        postbox = self.ubltr_get_field(
            env, ns, '//sh:Receiver/sh:Identifier')
        element_type = self.ubltr_get_field(
            env, ns, '//ef:Package/Elements/ElementType')

        _logger.debug("Processing Envelope UUID: %s" % uuid)

        if element_type == 'INVOICE':
            invoices = env.xpath('//ef:Package/Elements/ElementList'
                                 '/*[local-name() = "Invoice"]', namespaces=ns)
            for invoice in invoices:
                self.einvoice_process_invoice(
                    etree.tostring(invoice, encoding='utf-8', method='xml'),
                    sender, postbox, uuid)
        elif element_type == 'APPLICATIONRESPONSE':
            responses = env.xpath('//ef:Package/Elements/ElementList'
                                  '/*[local-name() = "ApplicationResponse"]',
                                  namespaces=ns)
            for response in responses:
                self.einvoice_process_response_document(
                    etree.tostring(response, encoding='utf-8', method='xml'),
                    document_type, uuid)

    # Get E-Invoice User List
    @api.model
    def einvoice_get_registered_users(self):
        if not self.l10n_tr_einvoice_user_download:
            return False
        if self.l10n_tr_einvoice_user_download_date == date.today():
            return True
        if len(self.l10n_tr_einvoice_sender_ids) == 0:
            raise UserError(_('Company has no sender(s)!'))
        params = self.einvoice_get_connect_params()
        identifier = self.l10n_tr_einvoice_sender_ids[0].name
        params['identifier'] = identifier
        params['part'] = self.l10n_tr_einvoice_user_download_sequence
        _logger.info("einvoice_get_registered_users %s" % identifier)
        endpoint = self._get_default_endpoint()
        result = iap_jsonrpc(endpoint + '/efatura/1/get_user_list_part',
                         params=params, timeout=1000)
        buffer = io.BytesIO()
        bytedata = base64.b64decode(result['data'])
        next_part = result['next']
        buffer.write(bytedata)

        if zipfile.is_zipfile(buffer):
            file = zipfile.ZipFile(buffer, 'r')
            for name in file.namelist():
                bytedata = file.read(name)
            reader = pycompat.csv_reader(io.BytesIO(bytedata),
                                         quotechar='"', delimiter=',')
            field_list = next(reader)
            users = [
                line for line in reader
                if any(line)
            ]
            # delete all registered users on first part
            if self.l10n_tr_einvoice_user_download_sequence == 1:
                _logger.info("Deleting E-Invoice Users:%s" % identifier)
                self._cr.execute(
                    "TRUNCATE TABLE l10n_tr_einvoice_user")

            _logger.info("Inserting E-Invoice Users: %s %d" %
                         (identifier, self.l10n_tr_einvoice_user_download_sequence))
            result = self.env['l10n_tr.einvoice.user'].load(field_list, users)
            if any(msg['type'] == 'error' for msg in result['messages']):
                warning_msg = "\n".join(msg['message'] for msg in result['messages'])
                raise UserError(warning_msg)
            _logger.info("Inserted E-Invoice Users: %s %d" %
                         (identifier, self.l10n_tr_einvoice_user_download_sequence))

            # save next part
            self.l10n_tr_einvoice_user_download_sequence = next_part

            # update all registered users on last part
            if next_part == 1:
                self.l10n_tr_einvoice_user_download_date = date.today()
                _logger.info("Updating E-Invoice Partners Started: %s" % identifier)
                self.env['res.partner'].search([])._compute_l10n_tr_einvoice_user()
                _logger.info("Updating E-Invoice Partners Completed: %s" % identifier)
        else:
            _logger.info("Invalid E-Invoice users zip file: %s" % identifier)

    # Get Incoming Invoices
    @api.model
    def einvoice_get_envelopes(self, identifier, document_type, from_date):
        now = datetime.now(pytz.timezone('Europe/Istanbul')) - relativedelta(minutes=2)
        from_date = from_date.replace(tzinfo=pytz.utc).astimezone(tz.gettz('Europe/Istanbul'))
        to_date = from_date + relativedelta(hours=12)
        if to_date > now:
            to_date = now
        list_params = self.einvoice_get_connect_params()
        list_params.update({
            'identifier': identifier,
            'document_type': document_type,
            'from_date': from_date.isoformat(),
            'to_date': to_date.isoformat(),
        })
        endpoint = self._get_default_endpoint()
        _logger.info("einvoice_get_envelopes %s %s %s" %
                     (identifier, from_date.isoformat(), to_date.isoformat()))
        ubl_list = iap_jsonrpc(endpoint + '/efatura/1/get_incoming_ubl_list',
                           params=list_params, timeout=120)
        ubl_params = self.einvoice_get_connect_params()
        ubl_params.update({
            'identifier': identifier,
            'direction': 'INBOUND',
        })

        # group of 20
        def chunker(seq, size):
            return (seq[pos:pos + size] for pos in range(0, len(seq), size))

        for group in chunker(ubl_list, 20):
            ubl_params['envelope_uuids'] = [d['uuid'] for d in group]
            ubls = iap_jsonrpc(endpoint + '/efatura/1/get_incoming_ubl',
                           params=ubl_params, timeout=120)
            for ubl in ubls:
                bytedata = base64.b64decode(ubl['envelope'])
                buffer = io.BytesIO(bytedata)
                if zipfile.is_zipfile(buffer):
                    file = zipfile.ZipFile(buffer, 'r')
                    for name in file.namelist():
                        bytedata = file.read(name)
                        _logger.debug("Processing Envelope: %s" %
                                      bytedata.decode('utf-8'))
                        self.einvoice_process_envelope(bytedata)
                else:
                    _logger.info("Invalid Zip File!")
        return to_date.astimezone(tz.gettz('UTC')).replace(tzinfo=None)
