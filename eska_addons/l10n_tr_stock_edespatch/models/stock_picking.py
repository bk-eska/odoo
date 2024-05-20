# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import uuid
import pytz
import base64
import zipfile
import io
import qrcode

from datetime import datetime
from dateutil.relativedelta import relativedelta

from lxml import etree
from lxml.etree import DocumentInvalid

import logging

_logger = logging.getLogger(__name__)

from odoo import _, api, fields, models
from odoo.addons.iap import jsonrpc
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import file_open


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    l10n_tr_document_type = fields.Selection(
        selection_add=[
            ('edespatch', 'E-Despatch'),
        ],
        ondelete={
            'edespatch': 'set default',
        },
    )

    l10n_tr_edespatch_uuid = fields.Char(
        string='UUID',
        readonly=True,
        copy=False,
    )

    l10n_tr_edespatch_envelope_uuid = fields.Char(
        string='Envelope UUID',
        readonly=True,
        copy=False,
        index=True,
    )

    l10n_tr_edespatch_response_uuid = fields.Char(
        string='Response UUID',
        readonly=True,
        copy=False,
        index=True,
    )

    l10n_tr_edespatch_state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('sent', 'Sent'),  # 1000, 1100, 1200, 1210, 1220 +
            ('waiting', 'Waiting Response'),  # kabul, red
            ('failed', 'Failed'),
            ('completed', 'Completed'),  # 1300 open
            ('rejected', 'Rejected'),
        ],
        string='E-Despatch Status',
        copy=False,
    )

    l10n_tr_edespatch_sender_id = fields.Many2one(
        comodel_name='l10n_tr.edespatch.sender',
        string='Sender',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
    )

    l10n_tr_edespatch_postbox_id = fields.Many2one(
        comodel_name='l10n_tr.edespatch.postbox',
        string='Postbox',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
    )

    l10n_tr_edespatch_sequence = fields.Many2one(
        comodel_name='ir.sequence',
        string='E-Despatch Number Sequence',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
    )

    l10n_tr_edespatch_candidate_sender_ids = fields.Many2many(
        comodel_name='l10n_tr.edespatch.sender',
        string='Candidate Senders',
        compute="_compute_edespatch_canditates",
    )

    l10n_tr_edespatch_candidate_postbox_ids = fields.Many2many(
        comodel_name='l10n_tr.edespatch.postbox',
        string='Candidate Postboxes',
        compute="_compute_edespatch_canditates",
    )

    l10n_tr_edespatch_zip = fields.Char(
        string='E-Despatch Zip Code',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
    )

    @api.depends("company_id", "partner_id", "l10n_tr_document_type")
    def _compute_edespatch_canditates(self):
        senders = self.env['l10n_tr.edespatch.sender']
        postboxes = self.env['l10n_tr.edespatch.postbox']
        for picking in self:
            if picking.l10n_tr_document_type == 'edespatch':
                if picking.picking_type_code == 'outgoing':
                    picking.l10n_tr_edespatch_candidate_sender_ids = senders.search([
                        ('company_id', '=', picking.company_id.id)])
                    if picking.partner_id.l10n_tr_edespatch_user:
                        picking.l10n_tr_edespatch_candidate_postbox_ids = postboxes.search([
                            ('partner_id', '=',
                             picking.partner_id.commercial_partner_id.id)])
                    else:
                        picking.l10n_tr_edespatch_candidate_postbox_ids = self.env.ref(
                            'l10n_tr_stock_edespatch.gib_postbox', False)
                elif picking.picking_type_code == 'incoming':
                    picking.l10n_tr_edespatch_candidate_sender_ids = senders.search([
                        ('partner_id', '=',
                         picking.partner_id.commercial_partner_id.id)])
                    picking.l10n_tr_edespatch_candidate_postbox_ids = postboxes.search([
                        ('company_id', '=', picking.company_id.id)])
                elif picking.picking_type_code == 'internal':
                    picking.l10n_tr_edespatch_candidate_sender_ids = senders.search([
                        ('company_id', '=', picking.company_id.id)])
                    picking.l10n_tr_edespatch_candidate_postbox_ids = postboxes.search([
                        ('company_id', '=', picking.company_id.id)])
                else:
                    picking.l10n_tr_edespatch_candidate_sender_ids = False
                    picking.l10n_tr_edespatch_candidate_postbox_ids = False
            else:
                picking.l10n_tr_edespatch_candidate_sender_ids = False
                picking.l10n_tr_edespatch_candidate_postbox_ids = False

    @api.model
    def _set_edespatch_vals(self):
        if self.company_id.l10n_tr_edespatch_enabled and self.company_id and \
                self.picking_type_id and self.l10n_tr_document_type == 'edespatch':
            partner = self.partner_id.commercial_partner_id
            if self.picking_type_code == 'outgoing':
                self.l10n_tr_edespatch_state = 'draft'
                self.l10n_tr_edespatch_sequence = \
                    self.picking_type_id.l10n_tr_edespatch_sequence
                self.l10n_tr_edespatch_sender_id = \
                    self.picking_type_id.l10n_tr_edespatch_sender_id
                if not partner.l10n_tr_edespatch_user:
                    self.l10n_tr_edespatch_postbox_id = self.env.ref(
                        'l10n_tr_stock_edespatch.gib_postbox', False)
                elif partner.l10n_tr_default_edespatch_postbox:
                    self.l10n_tr_edespatch_postbox_id = \
                        partner.l10n_tr_default_edespatch_postbox
                elif partner.l10n_tr_edespatch_postbox_ids:
                    self.l10n_tr_edespatch_postbox_id = \
                        partner.l10n_tr_edespatch_postbox_ids[0]
                else:
                    self.l10n_tr_edespatch_postbox_id = False
            elif self.picking_type_code == 'incoming':
                self.l10n_tr_edespatch_state = 'draft'
                self.l10n_tr_edespatch_sequence = False
                self.l10n_tr_edespatch_sender_id = False
                if self.picking_type_id.l10n_tr_edespatch_postbox_ids:
                    self.l10n_tr_edespatch_postbox_id = \
                        self.picking_type_id.l10n_tr_edespatch_postbox_ids[0]
                elif self.company_id.l10n_tr_edespatch_postbox_ids:
                    self.l10n_tr_edespatch_postbox_id = \
                        self.company_id.l10n_tr_edespatch_postbox_ids[0]
                else:
                        self.l10n_tr_edespatch_postbox_id = False
            elif self.picking_type_code == 'internal' and \
                    self.location_id.usage == 'internal' and \
                    self.location_dest_id.usage == 'internal':
                self.l10n_tr_edespatch_state = 'draft'
                self.l10n_tr_edespatch_sequence = \
                    self.picking_type_id.l10n_tr_edespatch_sequence
                self.l10n_tr_edespatch_sender_id = \
                    self.picking_type_id.l10n_tr_edespatch_sender_id
                if self.picking_type_id.l10n_tr_edespatch_postbox_ids:
                    self.l10n_tr_edespatch_postbox_id = \
                        self.picking_type_id.l10n_tr_edespatch_postbox_ids[0]
                elif self.company_id.l10n_tr_edespatch_postbox_ids:
                    self.l10n_tr_edespatch_postbox_id = \
                        self.company_id.l10n_tr_edespatch_postbox_ids[0]
                else:
                    self.l10n_tr_edespatch_postbox_id = False

        if self.l10n_tr_document_type != 'edespatch':
            self.l10n_tr_edespatch_state = False
            self.l10n_tr_edespatch_postbox_id = False
            self.l10n_tr_edespatch_sender_id = False
            self.l10n_tr_edespatch_sequence = False

    def _set_l10n_tr_document_type(self):
        for rec in self:
            partner = rec.partner_id.commercial_partner_id
            if rec.company_id.l10n_tr_edespatch_enabled and \
                    rec.company_id and self.picking_type_id:
                if rec.picking_type_code == 'outgoing' and partner:
                    rec.l10n_tr_document_type = 'edespatch'
                elif rec.picking_type_code == 'incoming' and partner:
                    if partner.l10n_tr_edespatch_user:
                        rec.l10n_tr_document_type = 'edespatch'
                else:
                    rec.l10n_tr_document_type = 'printed'
            else:
                rec.l10n_tr_document_type = 'printed'
            rec._set_edespatch_vals()

    @api.onchange('l10n_tr_document_type')
    def _onchange_l10n_tr_document_type(self):
        self._set_edespatch_vals()

    @api.model_create_multi
    def create(self, vals_list):
        pickings = super(StockPicking, self).create(vals_list)
        for picking, vals in zip(pickings, vals_list):
            if not vals.get('l10n_tr_document_type', False):
                picking._set_l10n_tr_document_type()
        return pickings

    @api.onchange('picking_type_id', 'partner_id', 'company_id',
                  'location_id', 'location_dest_id')
    def onchange_l10n_tr_document_type_fields(self):
        self._set_l10n_tr_document_type()

    def _action_done(self):
        for rec in self:
            if rec.picking_type_code in ['outgoing', 'internal'] and \
                    rec.company_id.l10n_tr_edespatch_enabled and \
                    rec.l10n_tr_document_type== 'edespatch':
                rec.date_done = fields.Datetime.now()
                rec.l10n_tr_document_number = \
                    rec.l10n_tr_edespatch_sequence.with_context(
                        ir_sequence_date=rec.date_done,
                        ir_sequence_date_range=rec.date_done)._next()
                if rec.picking_type_code == 'outgoing' and not rec.l10n_tr_date_despatch:
                    raise UserError(_('Please enter actual despatch date!'))
        result = super(StockPicking, self)._action_done()
        for rec in self:
            if rec.picking_type_code in ['outgoing', 'internal'] and \
                    rec.company_id.l10n_tr_edespatch_enabled and \
                    rec.l10n_tr_document_type== 'edespatch':
                rec.edespatch_send()
        return result

    @api.model
    def _get_xslt_params(self):
        img = qrcode.make(self.l10n_tr_edespatch_uuid).resize((100, 100))
        im_file = io.BytesIO()
        img.save(im_file, format="JPEG")
        im_bytes = im_file.getvalue()
        qr_base64 = base64.b64encode(im_bytes)
        return {
            'qrcode': qr_base64,
        }

    @api.model
    def edespatch_attach_pdf(self, ubl, xslt=False):
        try:
            pdf = self.env['ir.actions.reports']._render_qweb_pdf(
                'stock.report_deliveryslip', [self.id],
                {'xml': ubl, 'xslt': xslt})[0]
            attachment_vals = {
                'name': self.l10n_tr_document_number + '.pdf',
                'datas': base64.encodebytes(pdf),
                'res_model': 'stock.picking',
                'res_id': self.id,
                'type': 'binary',
                'company_id': self.company_id.id,
            }
            attachment = self.env['ir.attachment'].create(attachment_vals)
            self.message_post(attachment_ids=[attachment.id])
        except Exception as e:
            _logger.info("edespatch_attach_pdf failed: %s" % str(e))
            pass

    '''

    @api.returns('self')
    def refund(self, date_invoice=None, date=None, description=None, journal_id=None):
        res = super(AccountInvoice, self).refund(date_invoice, date, description, journal_id)
        res._set_edespatch_vals()
        return res

    '''

    @api.model
    def ubltr_generate_note_xml(self, parent, cbc, field):
        if field:
            for comment in field.splitlines():
                etree.SubElement(parent, '{%s}Note' % cbc).text = comment

    @api.model
    def edespatch_generate_order_xml(self, parent, cac, cbc):
        # this method is overridden to add order reference
        return True

    @api.model
    def edespatch_generate_additional_document_xml(self, parent, cac, cbc, issue_date):
        xsltref = etree.SubElement(parent, '{%s}AdditionalDocumentReference' % cac)
        etree.SubElement(xsltref, '{%s}ID' % cbc).text = "1"
        etree.SubElement(xsltref, '{%s}IssueDate' % cbc).text = issue_date
        etree.SubElement(xsltref, '{%s}DocumentTypeCode' % cbc).text = 'XSLT'
        etree.SubElement(xsltref, '{%s}DocumentType' % cbc).text = 'XSLT'
        attachment = etree.SubElement(xsltref, '{%s}Attachment' % cac)

        xslt = self.env['ir.actions.reports']._render_qweb_html(
            'stock.report_deliveryslip', [self.id], {'get_xslt': True})[0]
        if not xslt:
            raise ValidationError(_('Cannot find XSLT for this despatch!'))
        else:
            etree.SubElement(attachment, '{%s}EmbeddedDocumentBinaryObject' % cbc,
                             attrib={'characterSetCode': 'UTF-8',
                                     'encodingCode': 'Base64',
                                     'filename': '%s.xslt' % self.l10n_tr_document_number,
                                     'mimeCode': 'application/xml'}
                             ).text = base64.b64encode(xslt).decode()

    @api.model
    def edespatch_generate_shipment_stage_xml(self, parent, cac, cbc):
        if self.l10n_tr_driver_id and self.l10n_tr_vehicle_license_plate:
            stage = etree.SubElement(parent, '{%s}ShipmentStage' % cac)
            means = etree.SubElement(stage, '{%s}TransportMeans' % cac)
            road = etree.SubElement(means, '{%s}RoadTransport' % cac)
            etree.SubElement(road, '{%s}LicensePlateID' % cbc,
                             attrib={'schemeID': "PLAKA"}).text = \
                self.l10n_tr_vehicle_license_plate
            driver = etree.SubElement(stage, '{%s}DriverPerson' % cac)
            names = self.l10n_tr_driver_id.name.split()
            if len(names) < 2:
                raise UserError(_('Driver name error!'))
            lastname = names.pop()
            firstname = ' '.join(names)
            etree.SubElement(driver, '{%s}FirstName' % cbc).text = firstname
            etree.SubElement(driver, '{%s}FamilyName' % cbc).text = lastname
            etree.SubElement(driver, '{%s}Title' % cbc).text = "Şoför"
            if not self.l10n_tr_driver_id.vat:
                raise UserError(_('Driver TCKN missing!'))
            etree.SubElement(driver, '{%s}NationalityID' % cbc,
                             attrib={'schemeID': "TCKN"}).text = \
                self.l10n_tr_driver_id.vat

    @api.model
    def edespatch_generate_delivery_xml(self, parent, cac, cbc, issue_date, issue_time):
        delivery = etree.SubElement(parent, '{%s}Delivery' % cac)
        if not self.partner_id:
            raise UserError(_("E-Despatch requires delivery address!"))
        delivery_address = etree.SubElement(
            delivery, '{%s}DeliveryAddress' % cac)
        if not self.l10n_tr_edespatch_zip and not self.partner_id.zip:
            raise UserError(_("Delivery address doesn't have ZIP Code!"))
        self.partner_id.ubltr_generate_address_xml(
            delivery_address, cac, cbc, _('Delivery Address'), self.l10n_tr_edespatch_zip)
        if self.l10n_tr_transporter_id:
            self.l10n_tr_transporter_id.ubltr_generate_party_xml(
                'carrier', delivery, cac, cbc)
        despatch = etree.SubElement(delivery, '{%s}Despatch' % cac)
        actual_despatch = self.l10n_tr_date_despatch.replace(tzinfo=pytz.utc).astimezone(
                pytz.timezone('Europe/Istanbul')) if self.l10n_tr_date_despatch else False
        despatch_date = actual_despatch.strftime("%Y-%m-%d") if actual_despatch else issue_date
        despatch_time = actual_despatch.strftime("%H:%M:%S") if actual_despatch else issue_time
        etree.SubElement(despatch, '{%s}ActualDespatchDate' % cbc).text = despatch_date
        etree.SubElement(despatch, '{%s}ActualDespatchTime' % cbc).text = despatch_time

    @api.model
    def edespatch_generate_transport_handling_unit_xml(self, parent, cac, cbc):
        if self.l10n_tr_trailer_plate_no:
            transport_handling_unit = etree.SubElement(
                parent, '{%s}TransportHandlingUnit' % cac)
            transport_equipment = etree.SubElement(
                transport_handling_unit, '{%s}TransportEquipment' % cac)
            etree.SubElement(
                transport_equipment, '{%s}ID' % cbc, attrib={'schemeID': "DORSEPLAKA"}
            ).text = self.l10n_tr_trailer_plate_no

    @api.model
    def edespatch_generate_order_line_xml(self, parent, cac, cbc, line):
        etree.SubElement(parent, '{%s}LineID' % cbc)  # dummy

    def edespatch_generate_product_xml(self, item, cac, cbc, line):
        if 'product.customerinfo' in self.env:
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
                bii = etree.SubElement(item, '{%s}BuyersItemIdentification' % cac)
                etree.SubElement(bii, '{%s}ID' % cbc).text = bid.product_code
        if line.product_id.default_code:
            sii = etree.SubElement(item, '{%s}SellersItemIdentification' % cac)
            etree.SubElement(sii, '{%s}ID' % cbc).text = line.product_id.default_code

    @api.model
    def edespatch_get_buyer(self):
        return self.partner_id.parent_id or False

    @api.model
    def edespatch_generate_despatch_ubl_xml_etree(self):
        uom_precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        if not self.l10n_tr_edespatch_uuid:
            self.l10n_tr_edespatch_uuid = str(uuid.uuid4())
        xmlns = 'urn:oasis:names:specification:ubl:schema:xsd:DespatchAdvice-2'
        cac = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
        cbc = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
        ext = 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2'
        edespatch = etree.Element('{%s}DespatchAdvice' % xmlns,
                                  nsmap={
                                      None: xmlns,
                                      'cac': cac,
                                      'cbc': cbc,
                                      'ext': ext
                                  })
        etree.SubElement(edespatch, '{%s}UBLVersionID' % cbc).text = '2.1'
        etree.SubElement(edespatch, '{%s}CustomizationID' % cbc).text = 'TR1.2.1'
        etree.SubElement(edespatch, '{%s}ProfileID' % cbc).text = 'TEMELIRSALIYE'
        etree.SubElement(edespatch, '{%s}ID' % cbc).text = self.l10n_tr_document_number and self.l10n_tr_document_number or ''
        etree.SubElement(edespatch, '{%s}CopyIndicator' % cbc).text = 'false'
        etree.SubElement(edespatch, '{%s}UUID' % cbc).text = self.l10n_tr_edespatch_uuid
        if self.date_done:
            date_issue = self.date_done.replace(tzinfo=pytz.utc).astimezone(
                pytz.timezone('Europe/Istanbul'))
        else:
            date_issue = datetime.now(pytz.timezone('Europe/Istanbul'))
        if self.l10n_tr_date_despatch:
            actual_despatch = self.l10n_tr_date_despatch.replace(tzinfo=pytz.utc).astimezone(
                    pytz.timezone('Europe/Istanbul'))
            if actual_despatch < date_issue:
                date_issue = actual_despatch
        issue_date = date_issue.strftime("%Y-%m-%d")
        issue_time = date_issue.strftime("%H:%M:%S")
        etree.SubElement(edespatch, '{%s}IssueDate' % cbc).text = issue_date
        etree.SubElement(edespatch, '{%s}IssueTime' % cbc).text = issue_time
        etree.SubElement(edespatch, '{%s}DespatchAdviceTypeCode' % cbc).text = \
            'SEVK'
        notes = self.env["ir.fields.converter"].html_to_text(self.note)
        self.ubltr_generate_note_xml(edespatch, cbc, notes)

        self.edespatch_generate_order_xml(edespatch, cac, cbc)

        self.edespatch_generate_additional_document_xml(edespatch, cac, cbc, issue_date)

        commercial_partner = self.partner_id.commercial_partner_id

        buyer_party = False

        if self.picking_type_code == 'outgoing':
            accounting_party = 'company'
            supplier_party = self.company_id.partner_id
            customer_party = self.partner_id
            buyer_party = self.edespatch_get_buyer()
        elif self.picking_type_code == 'incoming':
            accounting_party = 'partner'
            supplier_party = commercial_partner
            customer_party = self.company_id.partner_id
        else:
            accounting_party = 'company'
            supplier_party = self.company_id.partner_id
            customer_party = self.company_id.partner_id

        supplier_address = False
        customer_address = False

        if self.picking_type_code == 'internal' and \
                self.location_id.usage == 'internal':
            source = self.env['stock.warehouse'].search([
                ('lot_stock_id', 'parent_of', self.location_id.id)], limit=1)
            if not source:
                raise UserError(_("Cannot find warehouse for location %s!") %
                                self.location_id.name)
            supplier_address = source.partner_id

        if self.picking_type_code == 'internal' and \
                self.location_dest_id.usage == 'internal':
            dest = self.env['stock.warehouse'].search([
                ('lot_stock_id', 'parent_of', self.location_dest_id.id)], limit=1)
            if not dest:
                raise UserError(_("Cannot find warehouse for location %s!") %
                                self.location_dest_id.name)
            customer_address = dest.partner_id

        company = etree.SubElement(edespatch, '{%s}DespatchSupplierParty' % cac)
        supplier_party.ubltr_generate_party_xml(
            'company', company, cac, cbc,
            commercial_partner.l10n_tr_party_identifiers,
            accounting_party, supplier_address)

        customer = etree.SubElement(edespatch, '{%s}DeliveryCustomerParty' % cac)
        customer_party.ubltr_generate_party_xml(
            'customer', customer, cac, cbc,
            commercial_partner.l10n_tr_party_identifiers,
            accounting_party, customer_address)

        if buyer_party:
            customer = etree.SubElement(edespatch, '{%s}BuyerCustomerParty' % cac)
            buyer_party.ubltr_generate_party_xml(
                'buyer', customer, cac, cbc,
                commercial_partner.l10n_tr_party_identifiers,
                accounting_party, customer_address)

        if not (self.l10n_tr_transporter_id or (self.l10n_tr_driver_id and
                                        self.l10n_tr_vehicle_license_plate)):
            raise UserError(_('Transport Company or Driver and '
                              'License Plate is missing!'))
        shipment = etree.SubElement(edespatch, '{%s}Shipment' % cac)
        etree.SubElement(shipment, '{%s}ID' % cbc).text = str(1)
        self.edespatch_generate_shipment_stage_xml(shipment, cac, cbc)
        self.edespatch_generate_delivery_xml(shipment, cac, cbc, issue_date, issue_time)
        self.edespatch_generate_transport_handling_unit_xml(shipment, cac, cbc)

        if len(self.move_line_ids) == 0:
            raise UserError(_('No move lines! Please Reserve or Validate!'))

        line_seq = 0
        for line in self.move_line_ids:
            line_seq += 1
            despatchline = etree.SubElement(edespatch, '{%s}DespatchLine' % cac)
            etree.SubElement(despatchline, '{%s}ID' % cbc).text = str(line_seq)
            etree.SubElement(despatchline, '{%s}DeliveredQuantity' % cbc,
                             attrib={'unitCode': line.product_uom_id.unece_code}).text \
                = '%.*f' % (uom_precision, line.qty_done)

            orderline = etree.SubElement(despatchline, '{%s}OrderLineReference' % cac)
            self.edespatch_generate_order_line_xml(orderline, cac, cbc, line)

            item = etree.SubElement(despatchline, '{%s}Item' % cac)
            description = line.product_id.display_name
            if line.move_id.description_picking:
                description += "\n%s" % line.move_id.description_picking
            if self.env.user.has_group('stock.group_lot_on_delivery_slip') and \
                    line.move_id.has_tracking and line.lot_id.name:
                description += "\n(%s)" % line.lot_id.name
            etree.SubElement(item, '{%s}Name' % cbc).text = description
            self.edespatch_generate_product_xml(item, cac, cbc, line)

        schema_file = file_open('l10n_tr_edi/data/xsd/maindoc/'
                                'UBL-DespatchAdvice-2.1-int.xsd')
        xmlschema_doc = etree.parse(schema_file)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        try:
            xmlschema.assertValid(edespatch)
        except DocumentInvalid as e:
            raise UserError(_("E-Despatch xsd validation failed!") + '\n\n' + e.args[0])
        return edespatch

    '''

    @api.model
    def edespatch_generate_receipt_ubl_xml_etree(self, response_type='accepted'):
        einvoice_uuid = str(uuid.uuid4())
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
        etree.SubElement(einvoice, '{%s}ProfileID' % cbc).text = self.einvoice_profile
        etree.SubElement(einvoice, '{%s}ID' % cbc).text = self.name
        etree.SubElement(einvoice, '{%s}UUID' % cbc).text = einvoice_uuid
        now = datetime.now(pytz.timezone('Europe/Istanbul'))
        etree.SubElement(einvoice, '{%s}IssueDate' % cbc).text = now.strftime("%Y-%m-%d")
        etree.SubElement(einvoice, '{%s}IssueTime' % cbc).text = now.strftime("%H:%M:%S")

        if self.type == 'out_invoice':
            accounting_party = 'company'
        else:
            accounting_party = 'partner'

        commercial_partner = self.partner_id.commercial_partner_id

        self.einvoice_generate_party_xml('sender', einvoice, cac, cbc, self.company_id.partner_id,
                                         commercial_partner.l10n_tr_party_identifiers, accounting_party)

        self.einvoice_generate_party_xml('receiver', einvoice, cac, cbc, commercial_partner,
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
        etree.SubElement(response, '{%s}ResponseCode' % cbc).text = response_code
        etree.SubElement(response, '{%s}Description' % cbc).text = response_desc

        doc_ref = etree.SubElement(doc_resp, '{%s}DocumentReference' % cac)
        etree.SubElement(doc_ref, '{%s}ID' % cbc).text = self.einvoice_uuid
        etree.SubElement(doc_ref, '{%s}IssueDate' % cbc).text = self.date_invoice.strftime("%Y-%m-%d")
        etree.SubElement(doc_ref, '{%s}DocumentTypeCode' % cbc).text = 'FATURA'
        etree.SubElement(doc_ref, '{%s}DocumentType' % cbc).text = 'FATURA'

        line_response = etree.SubElement(doc_resp, '{%s}LineResponse' % cac)
        line_reference = etree.SubElement(line_response, '{%s}LineReference' % cac)
        etree.SubElement(line_reference, '{%s}LineID' % cbc)
        response2 = etree.SubElement(line_response, '{%s}Response' % cac)
        etree.SubElement(response2, '{%s}ReferenceID' % cbc).text = '12345678911'
        etree.SubElement(response2, '{%s}ResponseCode' % cbc).text = response_code
        etree.SubElement(response2, '{%s}Description' % cbc).text = response_desc

        schema_file = file_open('l10n_tr_edi/data/xsd/maindoc/UBL-ApplicationResponse-2.1.xsd')
        xmlschema_doc = etree.parse(schema_file)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        try:
            xmlschema.assertValid(einvoice)
        except DocumentInvalid as e:
            raise UserError(_("E-Invoice xsd validation failed!") + '\n\n' + e.args[0])

        return einvoice

    '''
    ''' gerek yok gibi
    @api.model
    def edespatch_generate_despatch_ubl_xml_string(self, pretty_print=False):
        xml_tree = self.edespatch_generate_despatch_ubl_xml_etree()
        return etree.tostring(xml_tree,
                              encoding='utf-8',
                              method='xml',
                              pretty_print=pretty_print,
                              xml_declaration=False)
    '''

    # actions
    def action_edespatch_get_status(self):
        for despatch in self:
            despatch.edespatch_get_status()

    @api.model
    def edespatch_response_period_expired(self):
        oldest = datetime.now() - relativedelta(days=8)
        #  LK TODO kontrol et
        return self.create_date < oldest

    def action_edespatch_resend(self):
        for rec in self:
            if rec.picking_type_code in ['outgoing', 'internal'] and \
                    rec.l10n_tr_document_type== 'edespatch':
                rec.l10n_tr_edespatch_uuid = False
                rec.l10n_tr_edespatch_envelope_uuid = False
                rec.edespatch_send()

    # callbacks
    @api.model
    def action_edespatch_sent(self, message):
        if self.l10n_tr_edespatch_state != 'sent':
            self.write({'l10n_tr_edespatch_state': 'sent'})
            self.message_post(body=message)

    @api.model
    def action_edespatch_waiting(self, message):
        if self.l10n_tr_edespatch_state != 'waiting':
            self.write({'l10n_tr_edespatch_state': 'waiting'})
            self.message_post(body=message)

    @api.model
    def action_edespatch_completed(self, message):
        if self.l10n_tr_edespatch_state != 'completed':
            self.write({'l10n_tr_edespatch_state': 'completed'})
            self.message_post(body=message)

    @api.model
    def action_edespatch_failed(self, message):
        if self.l10n_tr_edespatch_state != 'failed':
            self.write({'l10n_tr_edespatch_state': 'failed'})
            self.message_post(body=message)

    # report_xslt hook methods
    @api.model
    def _get_xml_etree(self):
        return self.edespatch_generate_despatch_ubl_xml_etree()

    # Send E-Despatch
    @api.model
    def edespatch_send(self):
        for rec in self:
            if not rec.l10n_tr_edespatch_envelope_uuid:
                rec.l10n_tr_edespatch_envelope_uuid = str(uuid.uuid4())
            xml_tree = rec.edespatch_generate_despatch_ubl_xml_etree()
            data = self.company_id.ubltr_generate_envelope_xml(
                rec.l10n_tr_edespatch_envelope_uuid,
                'SENDERENVELOPE',
                rec.l10n_tr_edespatch_sender_id,
                rec.l10n_tr_edespatch_postbox_id,
                'DESPATCHADVICE',
                xml_tree)
            output = io.BytesIO()
            file = zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED)
            file.writestr('%s.xml' % rec.l10n_tr_edespatch_envelope_uuid, data)
            file.close()
            bytedata = base64.encodebytes(output.getvalue())
            params = self.company_id.einvoice_get_connect_params()
            params.update({
                'envelope': bytedata.decode(),
            })
            endpoint = self.company_id._get_default_endpoint()
            _logger.info("edespatch_send %s" % rec.l10n_tr_edespatch_sender_id.name)
            jsonrpc(endpoint + '/eirsaliye/1/send_ubl', params=params, timeout=120)
            if rec.picking_type_code == 'internal':
                # complete internal despatches and stop tracking
                rec.action_edespatch_completed(_('E-Despatch sent'))
            else:
                rec.action_edespatch_sent(_('E-Despatch sent'))
            # attach pdf
            self.edespatch_attach_pdf(xml_tree)

    # Query Invoice Status
    def edespatch_get_status(self):
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
            if group[0].picking_type_code == 'outgoing':
                identifier = group[0].l10n_tr_edespatch_sender_id.name
                uuids = group.mapped('l10n_tr_edespatch_envelope_uuid')
            else:
                identifier = group[0].l10n_tr_edespatch_postbox_id.name
                uuids = group.mapped('l10n_tr_edespatch_response_uuid')
            params['identifier'] = identifier
            params['envelope_uuids'] = uuids
            endpoint = self[0].company_id._get_default_endpoint()
            _logger.info("edespatch_get_status %s" % identifier)
            status_list = jsonrpc(endpoint + '/eirsaliye/1/get_envelope_status',
                                  params=params, timeout=120)
            for status in status_list:
                if status['response_code'] == '1300':
                    for rec in group:
                        if rec.l10n_tr_edespatch_envelope_uuid == status['envelope_uuid']:
                            if rec.partner_id.l10n_tr_edespatch_user:
                                rec.action_edespatch_waiting(
                                    _('E-Despatch transmitted'))
                            else:
                                rec.action_edespatch_completed(
                                    _('E-Despatch transmitted'))
                elif status['response_code'] not in ['1000', '1100', '1200', '1210', '1220']:
                    for rec in group:
                        if rec.l10n_tr_edespatch_envelope_uuid == status['envelope_uuid'] or \
                                rec.l10n_tr_edespatch_response_uuid == status['envelope_uuid']:
                            rec.action_edespatch_failed(
                                status['description'])

    '''
    # Send Response
    @api.model
    def edespatch_send_receipt(self):
        for rec in self:
            rec.l10n_tr_edespatch_response_uuid = str(uuid.uuid4())
            response_type = rec.edespatch_response_type
            xml_tree = rec.edespatch_generate_receipt_ubl_xml_etree(response_type)
            data = self.company_id.ubltr_generate_envelope_xml(
                rec.l10n_tr_edespatch_response_uuid,
                'POSTBOXENVELOPE',
                rec.l10n_tr_edespatch_postbox_id,
                rec.l10n_tr_edespatch_sender_id,
                'RECEIPTADVICE',
                xml_tree)
            output = io.BytesIO()
            file = zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED)
            file.writestr('%s.xml' % rec.l10n_tr_edespatch_response_uuid, data)
            file.close()
            bytedata = base64.encodebytes(output.getvalue())
            params = self.company_id.edespatch_get_connect_params()
            params.update({
                'envelope': bytedata.decode(),
            })
            endpoint = self.company_id._get_default_endpoint()
            _logger.info("edespatch_send_receipt %s" % self.name)
            jsonrpc(endpoint + '/eirsaliye/1/send_ubl', params=params, timeout=120)
            #  LK TODO ? sadece accept reject mi var?
            if response_type == 'accepted':
                rec.action_edespatch_sent(_('E-Despatch receipt sent (accepted)'))
            else:
                rec.action_edespatch_sent(_('E-Despatch receipt sent (rejected)'))
    '''
