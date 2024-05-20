# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import pytz
from datetime import datetime

from lxml import etree
import logging
_logger = logging.getLogger(__name__)

from odoo.exceptions import UserError

from odoo import _, api, models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_tr_edi_environment = fields.Selection(
        selection=[
            ('TEST', 'Test'),
            ('PROD', 'Production'),
        ],
        string='Environment',
        required=True,
        default='TEST',
    )

    @api.model
    def _get_default_endpoint(self):
        return 'https://www.eskayazilim.com.tr' \
            if self.l10n_tr_edi_environment == 'PROD' else 'http://localhost:8069'

    @api.model
    def einvoice_get_connect_params(self):
        if not self.vat:
            raise UserError(_('Please set company vat number!'))
        account = self.env['iap.account'].get_company_account('efatura', self)
        db_uuid = self.env['ir.config_parameter'].sudo().get_param(
            'database.uuid')
        tax_number = self.partner_id.ubltr_get_vat()
        params = {
            'db_uuid': db_uuid,
            'account_token': account.account_token,
            'tax_number': tax_number,
        }
        return params

    @api.model
    def ubltr_get_field(self, xml, ns, field):
        r = xml.xpath(field, namespaces=ns)
        if len(r) >= 1:
            if r[0].text:
                return r[0].text
        return False

    @api.model
    def ubltr_find_partner(self, einvoice, ns, tag):
        vk = self.ubltr_get_field(
            einvoice, ns, './cac:%s//cbc:ID[@schemeID="VKN"]' % tag)
        tc = self.ubltr_get_field(
            einvoice, ns, './cac:%s//cbc:ID[@schemeID="TCKN"]' % tag)

        if vk:
            is_company = True
            vat = vk
        elif tc:
            is_company = False
            vat = tc
        else:
            is_company = True
            vat = 'DUMMY'

        partner_id = self.env['res.partner'].search(
            [
                ('vat', 'in', [vat, 'TR'+vat]),
                ('company_id', 'in', [self.id, False]),
            ], order='parent_id desc, company_id asc', limit=1)

        if not partner_id:

            # create
            if is_company:
                name = self.ubltr_get_field(
                    einvoice, ns, '//cac:%s//cac:PartyName/cbc:Name' % tag)
            else:
                first = self.ubltr_get_field(
                    einvoice, ns, '//cac:%s//cbc:FirstName' % tag)
                middle = self.ubltr_get_field(
                    einvoice, ns, '//cac:%s//cbc:MiddleName' % tag)
                family = self.ubltr_get_field(
                    einvoice, ns, '//cac:%s//cbc:FamilyName' % tag)
                name = ' '.join(v for v in [first, middle, family] if v)

            partner = {
                'l10n_tr_einvoice_user': True,
                'name': name,
                'is_company': is_company,
                'company_id': self.id,
            }

            partner_id = self.env['res.partner'].with_context({}).create(partner)

            self._cr.execute('SAVEPOINT partner_create')

            # update
            partner = {
                'vat': vat,
            }
            if is_company:
                office = self.ubltr_get_field(
                    einvoice, ns, '//cac:%s//cac:TaxScheme/cbc:Name' % tag)
                if office:
                    off = self.env['account.tax.office'].search(
                        [
                            ('name', 'ilike', office.split()[0] + ' '),
                        ], limit=1)
                    if off:
                        partner['tax_office_id'] = off.id
            web = self.ubltr_get_field(
                einvoice, ns, '//cac:%s//cbc:WebsiteURI' % tag)
            if web:
                partner['website'] = web
            stn = self.ubltr_get_field(
                einvoice, ns, '//cac:%s//cbc:StreetName' % tag)
            blk = self.ubltr_get_field(
                einvoice, ns, '//cac:%s//cbc:BlockName' % tag)
            bld = self.ubltr_get_field(
                einvoice, ns, '//cac:%s//cbc:BuildingNumber' % tag)
            room = self.ubltr_get_field(
                einvoice, ns, '//cac:%s//cbc:Room' % tag)
            street = ' '.join(v for v in [stn, blk, bld, room] if v)
            if street:
                partner['street'] = street
            city = self.ubltr_get_field(
                einvoice, ns, '//cac:%s//cbc:CitySubdivisionName' % tag)
            if city:
                partner['city'] = city
            state = self.ubltr_get_field(
                einvoice, ns, '//cac:%s//cbc:CityName' % tag)
            if state:
                sta = self.env['res.country.state'].search(
                    [
                        ('name', 'ilike', state),
                    ], limit=1)
                if sta:
                    partner['state_id'] = sta.id

            zip = self.ubltr_get_field(
                einvoice, ns, '//cac:%s//cbc:PostalZone' % tag)
            if zip:
                partner['zip'] = zip
            country = self.ubltr_get_field(
                einvoice, ns, '//cac:%s//cac:Country/cbc:Name' % tag)
            if country:
                cnt = self.env['res.country'].search(
                    [
                        ('code', '=', country),
                    ], limit=1)
                if not cnt:
                    cnt = self.env['res.country'].search(
                        [
                            ('name', 'ilike', country),
                        ], limit=1)
                if cnt:
                    partner['country_id'] = cnt.id
            tel = self.ubltr_get_field(
                einvoice, ns, '//cac:%s//cbc:Telephone' % tag)
            if tel:
                partner['phone'] = tel
            email = self.ubltr_get_field(
                einvoice, ns, '//cac:%s//cbc:ElectronicMail' % tag)
            if email:
                partner['email'] = email

            try:
                partner_id.write(partner)
            except Exception:
                self._cr.execute('ROLLBACK TO SAVEPOINT partner_create')
                pass

        if partner_id and not partner_id.l10n_tr_einvoice_user:
            partner_id._compute_l10n_tr_einvoice_user()

        return partner_id

    @api.model
    def ubltr_find_product(self, line, ns, partner_id, buyer, seller):
        product_id = False
        sii = self.ubltr_get_field(
            line, ns, './cac:Item/cac:SellersItemIdentification/cbc:ID')
        if sii:
            if buyer:
                product_id = self.env['product.product'].search([
                    ('default_code', '=', sii)], limit=1)
            else:
                bid = self.env['product.supplierinfo'].search(
                    [
                        ('name', '=', partner_id.id),
                        ('product_code', '=', sii),
                        ('company_id', '=', self.id),
                    ], limit=1)
                if bid:
                    if bid.product_id:
                        product_id = bid.product_id
                    elif bid.product_tmpl_id.product_variant_ids:
                        product_id = bid.product_tmpl_id.product_variant_ids[0]

        bii = self.ubltr_get_field(
            line, ns, './cac:Item/cac:BuyersItemIdentification/cbc:ID')
        if bii and not product_id:
            if seller:
                product_id = self.env['product.product'].search([
                    ('default_code', '=', bii)], limit=1)
            else:
                sid = self.env['product.supplierinfo'].search(
                    [
                        ('name', '=', partner_id.id),
                        ('product_code', '=', bii),
                        ('company_id', '=', self.id),
                    ], limit=1)
                if sid:
                    if sid.product_id:
                        product_id = sid.product_id
                    elif sid.product_tmpl_id.product_variant_ids:
                        product_id = sid.product_tmpl_id.product_variant_ids[0]

        if not product_id:
            name = self.ubltr_get_field(line, ns, './cac:Item/cbc:Name')
            ps = self.env['product.supplierinfo'].search(
                [
                    ('name', '=', partner_id.id),
                    ('product_name', '=', name),
                    ('company_id', '=', self.id),
                ], limit=1)
            if ps:
                if ps.product_id:
                    product_id = ps.product_id
                elif ps.product_tmpl_id.product_variant_ids:
                    product_id = ps.product_tmpl_id.product_variant_ids[0]
        return product_id

    def ubltr_generate_envelope_xml(self, guid, type, sender, receiver, package_type, package):
        sh = 'http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader'
        ef = 'http://www.efatura.gov.tr/package-namespace'
        xsi = 'http://www.w3.org/2001/XMLSchema-instance'
        schema = 'PackageProxy_1_2.xsd'
        sbd = etree.Element('{%s}StandartBusinessDocument' % sh,
                            nsmap={
                                'sh': sh,
                                'ef': ef,
                                'xsi': xsi
                            },
                            attrib={
                                '{' + xsi + '}schemaLocation': sh + ' ' + schema
                            })
        header = etree.SubElement(sbd, '{%s}StandardBusinessDocumentHeader' % sh)
        etree.SubElement(header, '{%s}HeaderVersion' % sh).text = '1.0'

        sndr = etree.SubElement(header, '{%s}Sender' % sh)
        etree.SubElement(sndr, '{%s}Identifier' % sh).text = sender.name
        contact = etree.SubElement(sndr, '{%s}ContactInformation' % sh)
        etree.SubElement(contact, '{%s}Contact' % sh).text = sender.company_id.name
        etree.SubElement(contact, '{%s}ContactTypeIdentifier' % sh).text = 'UNVAN'
        contact = etree.SubElement(sndr, '{%s}ContactInformation' % sh)
        etree.SubElement(contact, '{%s}Contact' % sh).text = sender.company_id.partner_id.ubltr_get_vat()
        etree.SubElement(contact, '{%s}ContactTypeIdentifier' % sh).text = 'VKN_TCKN'

        if receiver.name == 'urn:mail:ihracatpk@gtb.gov.tr':
            rcvr = etree.SubElement(header, '{%s}Receiver' % sh)
            etree.SubElement(rcvr, '{%s}Identifier' % sh).text = 'urn:mail:ihracatpk@gtb.gov.tr'
            contact = etree.SubElement(rcvr, '{%s}ContactInformation' % sh)
            etree.SubElement(contact, '{%s}Contact' % sh).text = 'GÜMRÜK VE TİCARET BAKANLIĞI BİLGİ İŞLEM DAİRESİ BAŞKANLIĞI'
            etree.SubElement(contact, '{%s}ContactTypeIdentifier' % sh).text = 'UNVAN'
            contact = etree.SubElement(rcvr, '{%s}ContactInformation' % sh)
            etree.SubElement(contact, '{%s}Contact' % sh).text = '1460415308'
            etree.SubElement(contact, '{%s}ContactTypeIdentifier' % sh).text = 'VKN_TCKN'
        elif receiver.name == 'urn:mail:yolcuberaberpk@gtb.gov.tr':
            rcvr = etree.SubElement(header, '{%s}Receiver' % sh)
            etree.SubElement(rcvr, '{%s}Identifier' % sh).text = 'urn:mail:yolcuberaberpk@gtb.gov.tr'
            contact = etree.SubElement(rcvr, '{%s}ContactInformation' % sh)
            etree.SubElement(contact, '{%s}Contact' % sh).text = 'GÜMRÜK VE TİCARET BAKANLIĞI BİLGİ İŞLEM DAİRESİ BAŞKANLIĞI'
            etree.SubElement(contact, '{%s}ContactTypeIdentifier' % sh).text = 'UNVAN'
            contact = etree.SubElement(rcvr, '{%s}ContactInformation' % sh)
            etree.SubElement(contact, '{%s}Contact' % sh).text = '1460415308'
            etree.SubElement(contact, '{%s}ContactTypeIdentifier' % sh).text = 'VKN_TCKN'
        elif receiver.name == 'urn:mail:irsaliyepk@gib.gov.tr':
            rcvr = etree.SubElement(header, '{%s}Receiver' % sh)
            etree.SubElement(rcvr, '{%s}Identifier' % sh).text = 'urn:mail:irsaliyepk@gib.gov.tr'
            contact = etree.SubElement(rcvr, '{%s}ContactInformation' % sh)
            etree.SubElement(contact, '{%s}Contact' % sh).text = 'GİB'
            etree.SubElement(contact, '{%s}ContactTypeIdentifier' % sh).text = 'UNVAN'
            contact = etree.SubElement(rcvr, '{%s}ContactInformation' % sh)
            etree.SubElement(contact, '{%s}Contact' % sh).text = '3900892152'
            etree.SubElement(contact, '{%s}ContactTypeIdentifier' % sh).text = 'VKN_TCKN'
        else:
            receiver_partner = receiver.partner_id
            if not receiver_partner:
                receiver_partner = receiver.company_id.partner_id
            rcvr = etree.SubElement(header, '{%s}Receiver' % sh)
            etree.SubElement(rcvr, '{%s}Identifier' % sh).text = receiver.name
            contact = etree.SubElement(rcvr, '{%s}ContactInformation' % sh)
            etree.SubElement(contact, '{%s}Contact' % sh).text = receiver_partner.name
            etree.SubElement(contact, '{%s}ContactTypeIdentifier' % sh).text = 'UNVAN'
            contact = etree.SubElement(rcvr, '{%s}ContactInformation' % sh)
            etree.SubElement(contact, '{%s}Contact' % sh).text = receiver_partner.ubltr_get_vat()
            etree.SubElement(contact, '{%s}ContactTypeIdentifier' % sh).text = 'VKN_TCKN'

        docid = etree.SubElement(header, '{%s}DocumentIdentification' % sh)
        etree.SubElement(docid, '{%s}Standard' % sh).text = 'UBLTR'
        etree.SubElement(docid, '{%s}TypeVersion' % sh).text = '1.2'
        etree.SubElement(docid, '{%s}InstanceIdentifier' % sh).text = guid
        etree.SubElement(docid, '{%s}Type' % sh).text = type
        etree.SubElement(docid, '{%s}CreationDateAndTime' % sh).text = \
            datetime.now(pytz.timezone('Europe/Istanbul')).isoformat()

        pckg = etree.SubElement(sbd, '{%s}Package' % ef)
        elements = etree.SubElement(pckg, 'Elements')
        etree.SubElement(elements, 'ElementType').text = package_type
        etree.SubElement(elements, 'ElementCount').text = '1'
        elist = etree.SubElement(elements, 'ElementList')
        if package_type == 'INVOICE':
            xmlns = 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2'
            package.set('{' + xsi + '}schemaLocation', xmlns + ' UBLTR-Invoice-2.1.xsd')
        elif package_type == 'APPLICATIONRESPONSE':
            xmlns = 'urn:oasis:names:specification:ubl:schema:xsd:ApplicationResponse-2'
            package.set('{' + xsi + '}schemaLocation', xmlns + ' UBLTR-ApplicationResponse-2.1.xsd')
        elif package_type == 'DESPATCHADVICE':
            xmlns = 'urn:oasis:names:specification:ubl:schema:xsd:DespatchAdvice-2'
            package.set('{' + xsi + '}schemaLocation', xmlns + ' UBL-DespatchAdvice-2.1.xsd')
        elist.append(package)

        xmlstr = etree.tostring(sbd, encoding='utf-8',
                                method='xml', xml_declaration=True)
        return xmlstr
