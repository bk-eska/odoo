# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import re
from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_tr_party_identifiers = fields.One2many(
        comodel_name='l10n_tr.party.identification',
        inverse_name='partner_id',
        string='Party Identifiers',
        help='These identifiers are sent with e-documents.',
    )

    @api.model
    def ubltr_get_vat(self):
        vat = self.vat
        if vat:
            vat = re.sub(r'\W+', '', self.vat).upper()
            if vat[:2] == 'TR':
                vat = vat[2:]
        return vat

    @api.model
    def ubltr_generate_passport(self, parent, cac, cbc):
        # this method will be used to add passport information
        return

    @api.model
    def ubltr_generate_address_xml(self, parent, cac, cbc, prefix, zip=False):
        if self.street or self.street2:
            etree.SubElement(parent, '{%s}StreetName' % cbc).text = \
                ('%s %s' % (self.street or '', self.street2 or '')).strip()
        if not self.city:
            raise UserError(prefix + _("doesn't have city name!"))
        etree.SubElement(parent, '{%s}CitySubdivisionName' % cbc).text = self.city
        if not self.state_id:
            raise UserError(prefix + _("doesn't have state!"))
        etree.SubElement(parent, '{%s}CityName' % cbc).text = self.state_id.name
        if zip or self.zip:
            etree.SubElement(parent, '{%s}PostalZone' % cbc).text = zip or self.zip
        if not self.country_id:
            raise UserError(prefix + _("doesn't have country!"))
        country = etree.SubElement(parent, '{%s}Country' % cac)
        etree.SubElement(country, '{%s}Name' % cbc).text = self.country_id.name

    @api.model
    def ubltr_generate_party_xml(self, party_type, parent, cac, cbc, idts=[],
                                 accounting_party='company',
                                 physical_address=False, branch=False, passport=False):
        if party_type == 'customer':
            prefix = _('Partner') + ' '
            party_tag = 'Party'
        elif party_type == 'carrier':
            prefix = _('Carrier') + ' '
            party_tag = 'CarrierParty'
        elif party_type == 'signatory':
            prefix = _('Signatory') + ' '
            party_tag = 'SignatoryParty'
        elif party_type == 'sender':
            prefix = _('Sender') + ' '
            party_tag = 'SenderParty'
        elif party_type == 'receiver':
            prefix = _('Receiver') + ' '
            party_tag = 'ReceiverParty'
        elif party_type == 'branch':
            prefix = _('Branch') + ' '
            party_tag = 'AgentParty'
        elif party_type in ['export', 'taxfree', 'buyer']:
            prefix = _('Buyer') + ' '
            party_tag = 'Party'
        else:
            prefix = _('Company') + ' '
            party_tag = 'Party'

        party = etree.SubElement(parent, '{%s}%s' % (cac, party_tag))

        if self.website:
            etree.SubElement(party, '{%s}WebsiteURI' % cbc).text = self.website

        partyid = etree.SubElement(party, '{%s}PartyIdentification' % cac)

        commercial_partner = self.commercial_partner_id
        is_company = commercial_partner.company_type == 'company'

        if not self.country_id:
            raise UserError(prefix + _("doesn't have country!"))

        if party_type == 'export':
            etree.SubElement(partyid, '{%s}ID' % cbc,
                             attrib={'schemeID': 'PARTYTYPE'}).text = 'EXPORT'
            vat = '2222222222'
        elif party_type == 'taxfree':
            if is_company:
                raise UserError(prefix + _('must be a person!'))
            etree.SubElement(partyid, '{%s}ID' % cbc,
                             attrib={'schemeID': 'PARTYTYPE'}).text = 'TAXFREE'
        else:
            vat = self.ubltr_get_vat()
            if self.country_id.code == 'TR':
                if not vat:
                    if party_type not in ['customer', 'buyer'] and is_company:
                        raise UserError(prefix + _('tax number is missing!'))
                    else:
                        vat = '11111111111'
                if len(vat) == 10:
                    if not is_company and party_type != 'branch':
                        raise UserError(prefix + _('with VKN must be company!'))
                else:
                    #  http://forum.efatura.gov.tr/view.php?id=17077
                    if is_company:
                        raise UserError(prefix + _('with TCKN must be a person!'))
            else:
                if party_type in ['company', 'signatory', 'sender']:
                    raise UserError(prefix + _("address is not in Turkey!"))
                # International e-archive invoice
                vat = '2222222222' if is_company else '11111111111'

            if not vat.isdigit():
                raise UserError(prefix + _('tax number is not numeric!'))

            if is_company:
                etree.SubElement(partyid, '{%s}ID' % cbc,
                                 attrib={'schemeID': 'VKN'}).text = vat
            else:
                etree.SubElement(partyid, '{%s}ID' % cbc,
                                 attrib={'schemeID': 'TCKN'}).text = vat

        # company ids to send everyone
        if party_type == 'company':
            for idt in self.l10n_tr_party_identifiers:
                if idt.side == accounting_party:
                    partyid = etree.SubElement(party, '{%s}PartyIdentification' % cac)
                    etree.SubElement(partyid, '{%s}ID' % cbc,
                                     attrib={'schemeID': idt.party_identification}).text = idt.identifier

        for idt in idts:
            # company ids to send to this partner
            if party_type == 'company' and idt.side == accounting_party:
                partyid = etree.SubElement(party, '{%s}PartyIdentification' % cac)
                etree.SubElement(partyid, '{%s}ID' % cbc,
                                 attrib={'schemeID': idt.party_identification}).text = idt.identifier
            # customer ids to send to this partner
            if party_type == 'customer' and idt.side != accounting_party:
                partyid = etree.SubElement(party, '{%s}PartyIdentification' % cac)
                etree.SubElement(partyid, '{%s}ID' % cbc,
                                 attrib={'schemeID': idt.party_identification}).text = idt.identifier

        if is_company or party_type == 'export':
            partyname = etree.SubElement(party, '{%s}PartyName' % cac)
            if party_type == 'branch':
                etree.SubElement(partyname, '{%s}Name' % cbc).text = self.name
            else:
                etree.SubElement(partyname, '{%s}Name' % cbc).text = \
                    self.commercial_company_name or self.name

        postal_address = etree.SubElement(party, '{%s}PostalAddress' % cac)
        self.ubltr_generate_address_xml(postal_address, cac, cbc, prefix)

        if physical_address:
            physical_location = etree.SubElement(party, '{%s}PhysicalLocation' % cac)
            etree.SubElement(physical_location, '{%s}ID' % cbc).text = physical_address.name
            physical_location_address = etree.SubElement(physical_location, '{%s}Address' % cac)
            physical_address.ubltr_generate_address_xml(physical_location_address, cac, cbc, prefix)

        if is_company and self.country_id.code == 'TR' and party_type != 'branch':
            if not commercial_partner.tax_office_id:
                raise UserError(prefix + _("doesn't have tax office!"))
            partytaxscheme = etree.SubElement(party, '{%s}PartyTaxScheme' % cac)
            taxscheme = etree.SubElement(partytaxscheme, '{%s}TaxScheme' % cac)
            etree.SubElement(taxscheme, '{%s}Name' % cbc).text = commercial_partner.tax_office_id.name

        if is_company and party_type == 'export':
            legal_entity = etree.SubElement(party, '{%s}PartyLegalEntity' % cac)
            etree.SubElement(legal_entity,
                             '{%s}RegistrationName' % cbc).text = commercial_partner.commercial_company_name or commercial_partner.name
            etree.SubElement(legal_entity,
                             '{%s}CompanyID' % cbc).text = commercial_partner.vat or '2222222222'

        if self.phone or self.email:
            contact = etree.SubElement(party, '{%s}Contact' % cac)
            if self.phone:
                etree.SubElement(contact, '{%s}Telephone' % cbc).text = self.phone
            if self.email:
                etree.SubElement(contact, '{%s}ElectronicMail' % cbc).text = self.email

        if not is_company:
            person = etree.SubElement(party, '{%s}Person' % cac)
            names = self.name.split()
            if len(names) < 2:
                raise UserError(prefix + _('person name error!'))
            lastname = names.pop()
            firstname = ' '.join(names)
            etree.SubElement(person, '{%s}FirstName' % cbc).text = firstname
            etree.SubElement(person, '{%s}FamilyName' % cbc).text = lastname
            if party_type == 'customer' and passport:
                self.ubltr_generate_passport(parent, cac, cbc)
        if branch:
            branch.ubltr_generate_party_xml('branch', party, cac, cbc)
