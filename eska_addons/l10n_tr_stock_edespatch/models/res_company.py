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

    l10n_tr_edespatch_enabled = fields.Boolean(
        string='E-Despatch Enabled',
    )

    l10n_tr_edespatch_sender_ids = fields.One2many(
        comodel_name='l10n_tr.edespatch.sender',
        inverse_name='company_id',
        string='E-Despatch Senders',
        help='E-Despatch Senders for this company.',
    )

    l10n_tr_edespatch_postbox_ids = fields.One2many(
        comodel_name='l10n_tr.edespatch.postbox',
        inverse_name='company_id',
        string='E-Despatch Postboxes',
        help='E-Despatch Postboxes for this company.',
    )

    l10n_tr_edespatch_user_download = fields.Boolean(
        string='E-Despatch Registered User Update',
    )

    l10n_tr_edespatch_user_download_sequence = fields.Integer(
        string='E-Despatch Registered User Download Sequence',
        default=1,
    )

    l10n_tr_edespatch_user_download_date = fields.Date(
        string="E-Despatch Registered User Last Download Date",
    )

    @api.model
    def run_get_edespatch_users(self):
        company = self.search([
            ('l10n_tr_edespatch_user_download', '=', True)
        ], limit=1)
        if company:
            company.edespatch_get_registered_users()

    @api.model
    def run_get_edespatch_despatches(self):
        for company in self.search([('l10n_tr_edespatch_enabled', '=', True)]):
            company.with_context(lang='tr_TR').l10n_tr_edespatch_postbox_ids.get_despatches()

    @api.model
    def run_get_edespatch_receipts(self):
        for company in self.search([('l10n_tr_edespatch_enabled', '=', True)]):
            company.with_context(lang='tr_TR').l10n_tr_edespatch_sender_ids.get_receipts()

    @api.model
    def run_update_edespatches(self):
        for company in self.search([('l10n_tr_edespatch_enabled', '=', True)]):
            company.l10n_tr_edespatch_sender_ids.update_despatches()
            company.l10n_tr_edespatch_postbox_ids.update_despatches()

    @api.model
    def edespatch_process_despatch_lines(self, edespatch, ns, picking,
                                       partner_id):

        self._cr.execute('SAVEPOINT despatch_lines_create')

        try:
            lines = edespatch.xpath('./cac:DespatchLine', namespaces=ns)
            for line in lines:
                seq = self.ubltr_get_field(line, ns, './cbc:ID')
                iq = line.xpath('./cbc:DeliveredQuantity', namespaces=ns)[0]
                qty = float(iq.text)
                uom_code = iq.get("unitCode")
                uom_id = self.env['uom.uom'].search([
                    ('unece_code', '=', uom_code)], limit=1)
                name = self.ubltr_get_field(
                    line, ns, './cac:Item/cbc:Name')
                desc = self.ubltr_get_field(
                    line, ns, './cac:Item/cbc:Description')
                if desc:
                    name = name + ' ' + desc

                product_id = self.ubltr_find_product(self,
                    line, ns, partner_id, True, True)

                if product_id:
                    rec = {
                        'company_id': self.id,
                        'picking_id': picking.id,
                        'quantity': qty,
                        'sequence': seq,
                        'product_uom': seq,
                        'name': name,
                        'product_id': product_id.id,
                    }

                    if uom_id:
                        rec['uom_id'] = uom_id.id

                    self.env['stock.move'].sudo().with_context(
                        force_company=rec.get('company_id', False)).create(rec)

        except Exception:
            # if something happens rollback line inserts
            self._cr.execute('ROLLBACK TO SAVEPOINT despatch_lines_create')
            pass

    @api.model
    def edespatch_process_despatch(self, ubl, sender, postbox, envelope_uuid):

        _logger.info("edespatch_process_despatch %s %s %s" %
                     (sender, postbox, envelope_uuid))
        ns = {
            'cac': "urn:oasis:names:specification:ubl:schema:xsd:"
                   "CommonAggregateComponents-2",
            'cbc': "urn:oasis:names:specification:ubl:schema:xsd:"
                   "CommonBasicComponents-2",
        }

        parser = etree.XMLParser(recover=True)
        edespatch = etree.fromstring(ubl, parser)

        schema_file = file_open('l10n_tr_edi/data/xsd/maindoc/'
                                'UBL-DespatchAdvice-2.1.xsd')
        xmlschema_doc = etree.parse(schema_file)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        try:
            xmlschema.assertValid(edespatch)
        except DocumentInvalid as e:
            _logger.error("E-despatch xsd validation failed!" + '\n\n' + e.args[0])
            pass
        '''
        type_code = self.ubltr_get_field(edespatch, ns,
                                         './cbc:DespatchAdviceTypeCode')
        '''
        partner_id = self.ubltr_find_partner(edespatch, ns, 'DespatchSupplierParty')

        if partner_id.vat == self.vat:
            return  # ignore internal despatches

        number = self.ubltr_get_field(edespatch, ns, './cbc:ID')
        issue_date = self.ubltr_get_field(edespatch, ns, './cbc:IssueDate')
        issue_time = self.ubltr_get_field(edespatch, ns, './cbc:IssueTime')
        issue_time = issue_time[:8]
        date_issue = datetime.strptime(issue_date + ' ' + issue_time,
                                       '%Y-%m-%d %H:%M:%S')
        uuid = self.ubltr_get_field(edespatch, ns, './cbc:UUID')
        despatch_date = self.ubltr_get_field(
            edespatch, ns,
            './cac:Shipment/cac:Delivery/cac:Despatch/cbc:ActualDespatchDate')
        despatch_time = self.ubltr_get_field(
            edespatch, ns,
            './cac:Shipment/cac:Delivery/cac:Despatch/cbc:ActualDespatchTime')
        despatch_time = despatch_time[:8]
        l10n_tr_date_despatch = datetime.strptime(despatch_date + ' ' + despatch_time,
                                       '%Y-%m-%d %H:%M:%S')

        picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'incoming'),
            ('company_id', '=', self.id)
        ], limit=1)

        if picking_type.default_location_src_id:
            location_id = picking_type.default_location_src_id.id
        else:
            location_id = self.env.ref('stock.stock_location_suppliers').id

        if picking_type.default_location_dest_id:
            location_dest_id = picking_type.default_location_dest_id.id
        else:
            location_dest_id = self.env.ref('stock.stock_location_stock').id

        rec = {
            'company_id': self.id,
            'l10n_tr_document_number': number,
            'move_type': 'direct',
            'picking_type_id': picking_type.id,
            'location_id': location_id,
            'location_dest_id': location_dest_id,
            'scheduled_date': date_issue,
            'l10n_tr_date_despatch': l10n_tr_date_despatch,
            'l10n_tr_document_type': 'edespatch',
            'l10n_tr_edespatch_uuid': uuid,
            'l10n_tr_edespatch_envelope_uuid': envelope_uuid,
            'partner_id': partner_id.id
        }

        if sender:
            sender_id = self.env['l10n_tr.edespatch.sender'].search([
                ('partner_id', '=', partner_id.id),
                ('name', '=', sender),
            ], limit=1)
            if not sender_id:
                sender_id = self.env['l10n_tr.edespatch.sender'].\
                    with_context({}).create({
                    'partner_id': partner_id.id,
                    'name': sender,
                })
            rec['l10n_tr_edespatch_sender_id'] = sender_id.id

        if postbox:
            postbox_id = self.env['l10n_tr.edespatch.postbox'].search([
                ('company_id', '=', self.id),
                ('name', '=', postbox),
            ], limit=1)
            if postbox_id:
                rec['l10n_tr_edespatch_postbox_id'] = postbox_id.id
                if postbox_id.picking_type_id:
                    rec['picking_type_id'] = postbox_id.picking_type_id.id

        comment = ''
        notes = edespatch.xpath('./cbc:Note', namespaces=ns)
        for note in notes:
            if note.text:
                comment += note.text
                comment += '\n'

        if comment:
            rec['note'] = comment

        reference = self.ubltr_get_field(
            edespatch, ns, "./cac:OrderReference/cbc:ID")
        if reference:
            rec['origin'] = reference

        picking = self.env['stock.picking'].with_context({}).create(rec)

        self.edespatch_process_despatch_lines(edespatch, ns, picking, partner_id)

        picking.action_edespatch_waiting(_('E-Despatch waiting response'))

        try:
            xslt = self.ubltr_get_field(
                edespatch, ns, "./cac:AdditionalDocumentReference/"
                              "cbc:DocumentType[translate"
                              "(.,'xslt','XSLT') = 'XSLT']/"
                              "../cac:Attachment/"
                              "cbc:EmbeddedDocumentBinaryObject")
            if not xslt:
                xslt = self.ubltr_get_field(
                    edespatch, ns, "./cac:AdditionalDocumentReference/"
                                  "cac:Attachment/"
                                  "cbc:EmbeddedDocumentBinaryObject[contains"
                                  "(translate(@filename,'xslt','XSLT'),'XSLT')]")
            if xslt:
                xslt_etree = etree.fromstring(base64.b64decode(xslt))
                picking.edespatch_attach_pdf(edespatch, xslt_etree)
        except Exception:
            pass

    @api.model
    def edespatch_process_receipt(self, ubl, document_type, envelope_uuid):

        _logger.info("edespatch_process_response %s %s" %
                     (document_type, envelope_uuid))

        ns = {
            'cac': "urn:oasis:names:specification:ubl:schema:xsd:"
                   "CommonAggregateComponents-2",
            'cbc': "urn:oasis:names:specification:ubl:schema:xsd:"
                   "CommonBasicComponents-2",
        }

        parser = etree.XMLParser(recover=True)
        response = etree.fromstring(ubl, parser)

        schema_file = file_open('l10n_tr_edi/data/xsd/maindoc/'
                                'UBL-ReceiptAdvice-2.1.xsd')
        xmlschema_doc = etree.parse(schema_file)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        try:
            xmlschema.assertValid(response)
        except DocumentInvalid as e:
            _logger.error("E-Despatch response xsd validation failed!\n" + e.args[0])
            pass

        uuid = self.ubltr_get_field(
            response, ns, './cac:DespatchDocumentReference/cbc:ID')
        if not uuid:
            return
        picking = self.env['stock.picking'].search([
            ('l10n_tr_edespatch_uuid', '=', uuid)], limit=1)
        if not picking:
            _logger.error("E-Despatch not found! UUID=" + uuid)
        else:
            description = ''
            notes = response.xpath('./cbc:Note', namespaces=ns)
            for note in notes:
                if note.text:
                    description += note.text
                    description += '\n'
            if not description:
                description = _('E-Despatch response received!')
            picking.l10n_tr_edespatch_response_uuid = envelope_uuid
            picking.action_edespatch_completed(description)
            try:
                xslt = self.ubltr_get_field(
                    response, ns, "./cac:AdditionalDocumentReference/"
                                  "cbc:DocumentType[translate"
                                  "(.,'xslt','XSLT') = 'XSLT']/"
                                  "../cac:Attachment/"
                                  "cbc:EmbeddedDocumentBinaryObject")
                if not xslt:
                    xslt = self.ubltr_get_field(
                        response, ns, "./cac:AdditionalDocumentReference/"
                                      "cac:Attachment/"
                                      "cbc:EmbeddedDocumentBinaryObject[contains"
                                      "(translate(@filename,'xslt','XSLT'),'XSLT')]")
                if xslt:
                    xslt_etree = etree.fromstring(base64.b64decode(xslt))
                    picking.edespatch_attach_pdf(response, xslt_etree)
            except Exception:
                pass

    @api.model
    def edespatch_process_envelope(self, envelope):
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

        if element_type == 'DESPATCHADVICE':
            despatches = env.xpath('//ef:Package/Elements/ElementList'
                                 '/*[local-name() = "DespatchAdvice"]',
                                 namespaces=ns)
            for despatch in despatches:
                self.edespatch_process_despatch(
                    etree.tostring(despatch, encoding='utf-8', method='xml'),
                    sender, postbox, uuid)
        elif element_type == 'RECEIPTADVICE':
            responses = env.xpath('//ef:Package/Elements/ElementList'
                                  '/*[local-name() = "ReceiptAdvice"]',
                                  namespaces=ns)
            for response in responses:
                self.edespatch_process_receipt(
                    etree.tostring(response, encoding='utf-8', method='xml'),
                    document_type, uuid)

    # Get E-Dispatch User List
    @api.model
    def edespatch_get_registered_users(self):
        if not self.l10n_tr_edespatch_user_download:
            return False
        if self.l10n_tr_edespatch_user_download_date == date.today():
            return True
        if len(self.l10n_tr_edespatch_sender_ids) == 0:
            raise UserError(_('Company has no sender(s)!'))
        params = self.einvoice_get_connect_params()
        identifier = self.l10n_tr_edespatch_sender_ids[0].name
        params['identifier'] = identifier
        params['part'] = self.l10n_tr_edespatch_user_download_sequence
        _logger.info("edespatch_get_registered_users %s" % identifier)
        endpoint = self._get_default_endpoint()
        result = iap_jsonrpc(endpoint + '/eirsaliye/1/get_user_list_part',
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
            if self.l10n_tr_edespatch_user_download_sequence == 1:
                _logger.info("Deleting E-Despatch Users:%s" % identifier)
                self._cr.execute(
                    "TRUNCATE TABLE l10n_tr_edespatch_user")

            _logger.info("Inserting E-Despatch Users: %s %d" %
                         (identifier, self.l10n_tr_edespatch_user_download_sequence))
            result = self.env['l10n_tr.edespatch.user'].load(
                field_list, users)
            if any(msg['type'] == 'error' for msg in result['messages']):
                warning_msg = "\n".join(msg['message'] for msg in result['messages'])
                raise UserError(warning_msg)
            _logger.info("Inserted E-Despatch Users: %s %d" %
                         (identifier, self.l10n_tr_edespatch_user_download_sequence))

            # save next part
            self.l10n_tr_edespatch_user_download_sequence = next_part

            # update all registered users on last part
            if next_part == 1:
                self.l10n_tr_edespatch_user_download_date = date.today()
                _logger.info("Updating E-Despatch Partners Started: %s" % identifier)
                self.env['res.partner'].search([])._compute_l10n_tr_edespatch_user()
                _logger.info("Updating E-Despatch Partners Completed: %s" % identifier)
        else:
            _logger.info("Invalid E-Despatch users zip file: %s" % identifier)

    # Get Incoming Envelopes
    @api.model
    def edespatch_get_envelopes(self, identifier, document_type, from_date):
        now = datetime.now(pytz.timezone('Europe/Istanbul'))
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
        _logger.info("edespatch_get_envelopes %s %s %s" %
                     (identifier, from_date.isoformat(), to_date.isoformat()))
        ubl_list = iap_jsonrpc(endpoint + '/eirsaliye/1/get_incoming_ubl_list',
                           params=list_params)
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
            ubls = iap_jsonrpc(endpoint + '/eirsaliye/1/get_incoming_ubl',
                           params=ubl_params)
            for ubl in ubls:
                bytedata = base64.b64decode(ubl['envelope'])
                buffer = io.BytesIO(bytedata)
                if zipfile.is_zipfile(buffer):
                    file = zipfile.ZipFile(buffer, 'r')
                    for name in file.namelist():
                        bytedata = file.read(name)
                        _logger.debug("Processing Envelope: %s" %
                                      bytedata.decode('utf-8'))
                        self.edespatch_process_envelope(bytedata)
                else:
                    _logger.info("Invalid Zip File!")
        return to_date.astimezone(tz.gettz('UTC')).replace(tzinfo=None)

