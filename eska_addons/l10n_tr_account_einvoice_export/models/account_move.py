# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_tr_einvoice_profile = fields.Selection(
        selection_add=[
            ('IHRACAT', 'İhracat'),
            ('YOLCUBERABERFATURA', 'Yolcu Beraberinde Fatura'),
        ],
    )

    l10n_tr_einvoice_gtb_refno = fields.Char(
        string='GTB Ref No',
        readonly=True,
        copy=False,
    )

    l10n_tr_einvoice_gtb_gcb_tescilno = fields.Char(
        string='GCB Tescil No',
        readonly=True,
        copy=False,
    )

    l10n_tr_einvoice_gtb_export_date = fields.Date(
        string='GTB Export Date',
        readonly=True,
        copy=False,
    )

    l10n_tr_transport_mode_code = fields.Selection(
        selection=[
            ('1', 'Maritime transport'),
            ('2', 'Rail transport'),
            ('3', 'Road transport'),
            ('4', 'Air transport'),
            ('5', 'Mail'),
            ('6', 'Multimodal transport'),
            ('7', 'Fixed transport installations'),
            ('8', 'Inland water transport'),
        ],
        string='Transport Mode',
    )

    def _must_check_constrains_date_sequence(self):
        if self.l10n_tr_einvoice_gtb_export_date:
            return False
        else:
            return super(AccountMove, self)._must_check_constrains_date_sequence()

    def _get_l10n_tr_default_einvoice_postbox(self):
        if self.fiscal_position_id.l10n_tr_fp_code == '301' and \
                self.move_type == 'out_invoice':
            export = self.env.ref(
                'l10n_tr_account_einvoice_export.gib_export', False)
            taxfree = self.env.ref(
                'l10n_tr_account_einvoice_export.gib_taxfree', False)
            if self.l10n_tr_einvoice_profile == 'IHRACAT':
                return export
            elif self.l10n_tr_einvoice_profile == 'YOLCUBERABERFATURA':
                return taxfree
        return super(AccountMove, self)._get_l10n_tr_default_einvoice_postbox()

    def _get_l10n_tr_default_einvoice_profile(self):
        if self.fiscal_position_id.l10n_tr_default_export_type:
            return self.fiscal_position_id.l10n_tr_default_export_type
        else:
            return super(AccountMove, self)._get_l10n_tr_default_einvoice_profile()

    @api.model
    def _set_l10n_tr_delivery_type(self):
        result = super(AccountMove, self)._set_l10n_tr_delivery_type()
        for rec in self:
            if rec.company_id.l10n_tr_einvoice_enabled and \
                    rec.fiscal_position_id.l10n_tr_default_export_type == 'IHRACAT':
                rec.l10n_tr_delivery_type = 'einvoice'
        return result

    @api.onchange('fiscal_position_id')
    def _onchange_fiscal_position_id(self):
        self._set_l10n_tr_delivery_type()
        self._set_einvoice_vals()

    @api.model
    def einvoice_get_invoice_lines(self):
        lines = super(AccountMove, self).einvoice_get_invoice_lines()
        if self.l10n_tr_einvoice_profile == 'IHRACAT':
            lines = lines.filtered(
                lambda l: not l.product_id.l10n_tr_einvoice_shipment_cost
                          and not l.product_id.l10n_tr_einvoice_insurance_cost)
        return lines

    @api.model
    def einvoice_generate_ubl_xml_etree(self):
        if self.l10n_tr_einvoice_profile == 'IHRACAT' and \
                self.fiscal_position_id.l10n_tr_fp_code != '301':
            raise UserError(_("Export Fiscal Position (301) is "
                              "required with this profile!"))
        if self.l10n_tr_einvoice_profile == 'YOLCUBERABERFATURA' and \
                self.fiscal_position_id.l10n_tr_fp_code != '501':
            raise UserError(_("Export Fiscal Position (501) is "
                              "required with this profile!"))
        return super(AccountMove, self).einvoice_generate_ubl_xml_etree()

    @api.model
    def einvoice_generate_invoice_line_note_xml(self, invoice_line, cac, cbc, line):
        super().einvoice_generate_invoice_line_note_xml(invoice_line, cac, cbc, line)
        if self.l10n_tr_einvoice_profile == 'IHRACAT':
            etree.SubElement(invoice_line, '{%s}Note' % cbc).text = \
                line.product_id.with_context(lang='tr_TR').display_name

    @api.model
    def einvoice_generate_product_xml(self, item, cac, cbc, line):
        super().einvoice_generate_product_xml(item, cac, cbc, line)
        if self.l10n_tr_einvoice_profile == 'IHRACAT':
            if line.product_id.country_of_origin:
                sii = etree.SubElement(item, '{%s}OriginCountry' % cac)
                etree.SubElement(sii, '{%s}Name' % cbc).text = \
                    line.product_id.country_of_origin.name
            if line.product_id.hs_code:
                cc = etree.SubElement(item, '{%s}CommodityClassification' % cac)
                etree.SubElement(cc, '{%s}ItemClassificationCode' % cbc).text = \
                    line.product_id.hs_code

    @api.model
    def einvoice_accounting_customer_party_xml(self, einvoice, cac, cbc,
                                               commercial_partner,
                                               accounting_party):

        if self.l10n_tr_einvoice_profile in ['IHRACAT', 'YOLCUBERABERFATURA']:
            gib = etree.SubElement(einvoice,
                                        '{%s}AccountingCustomerParty' % cac)
            party = etree.SubElement(gib, '{%s}%s' % (cac, 'Party'))
            etree.SubElement(party, '{%s}WebsiteURI' % cbc)
            partyid = etree.SubElement(party, '{%s}PartyIdentification' % cac)
            etree.SubElement(partyid, '{%s}ID' % cbc,
                             attrib={'schemeID': 'VKN'}).text = '1460415308'
            partyname = etree.SubElement(party, '{%s}PartyName' % cac)
            etree.SubElement(partyname, '{%s}Name' % cbc).text = \
                'Gümrük ve Ticaret Bakanlığı Gümrükler Genel Müdürlüğü- ' \
                'Bilgi İşlem Dairesi Başkanlığı'
            postal_address = etree.SubElement(party, '{%s}PostalAddress' % cac)
            etree.SubElement(postal_address, '{%s}CitySubdivisionName' % cbc)
            etree.SubElement(postal_address,
                             '{%s}CityName' % cbc).text = 'Ankara'
            country = etree.SubElement(postal_address, '{%s}Country' % cac)
            etree.SubElement(country, '{%s}Name' % cbc).text = 'Türkiye'
            partytaxscheme = etree.SubElement(party, '{%s}PartyTaxScheme' % cac)
            taxscheme = etree.SubElement(partytaxscheme, '{%s}TaxScheme' % cac)
            etree.SubElement(taxscheme, '{%s}Name' % cbc).text = 'Ulus'
            buyer = etree.SubElement(einvoice, '{%s}BuyerCustomerParty' % cac)
            type = 'export' if self.l10n_tr_einvoice_profile == 'IHRACAT' else 'taxfree'
            passport = self.l10n_tr_einvoice_profile == 'YOLCUBERABERFATURA'
            commercial_partner.ubltr_generate_party_xml(
                type, buyer, cac, cbc, passport=passport)
        else:
            return super(AccountMove,
                         self).einvoice_accounting_customer_party_xml(
                einvoice, cac, cbc, commercial_partner, accounting_party)

    @api.model
    def einvoice_generate_delivery_terms_xml(self, parent, cac, cbc):
        super().einvoice_generate_delivery_terms_xml(parent, cac, cbc)
        if self.l10n_tr_einvoice_profile == 'IHRACAT':
            if not self.invoice_incoterm_id:
                raise UserError(_("Export invoices require incoterms!"))
            delivery_terms = etree.SubElement(
                parent, '{%s}DeliveryTerms' % cac)
            etree.SubElement(delivery_terms, '{%s}ID' % cbc,
                             attrib={'schemeID': 'INCOTERMS'}).text = \
                self.invoice_incoterm_id.code
            etree.SubElement(delivery_terms, '{%s}SpecialTerms' % cbc).text = \
                self.invoice_incoterm_id.name

    @api.model
    def einvoice_generate_shipment_xml(self, parent, cac, cbc, picking):
        shipment = super().einvoice_generate_shipment_xml(parent, cac, cbc,
                                                          picking)
        if self.l10n_tr_einvoice_profile == 'IHRACAT':
            price_precision = self.env['decimal.precision'].precision_get(
                'Product Price')
            insurance_amount = sum(self.invoice_line_ids.filtered(
                lambda line: line.product_id.l10n_tr_einvoice_insurance_cost
            ).mapped('price_total'))
            if insurance_amount > 0.0:
                etree.SubElement(
                    shipment, '{%s}InsuranceValueAmount' % cbc,
                    attrib={'currencyID': self.currency_id.name}).text = \
                    '%.*f' % (price_precision, insurance_amount)
            shipment_amount = sum(self.invoice_line_ids.filtered(
                lambda line: line.product_id.l10n_tr_einvoice_shipment_cost
            ).mapped('price_total'))
            if shipment_amount > 0.0:
                etree.SubElement(
                    shipment, '{%s}DeclaredForCarriageValueAmount' % cbc,
                    attrib={'currencyID': self.currency_id.name}).text = \
                    '%.*f' % (price_precision, shipment_amount)

    @api.model
    def einvoice_generate_delivery_line_xml(self, parent, line, price_precision,
                                            line_price_unit, cac, cbc):
        super().einvoice_generate_delivery_line_xml(
            parent, line, price_precision, line_price_unit, cac, cbc)
        if self.l10n_tr_einvoice_profile == 'IHRACAT':
            delivery = etree.SubElement(parent, '{%s}Delivery' % cac)
            if not self.partner_shipping_id:
                raise UserError(_("Export invoices require shipping address!"))
            delivery_address = etree.SubElement(
                delivery, '{%s}DeliveryAddress' % cac)
            self.partner_shipping_id.ubltr_generate_address_xml(
                delivery_address, cac, cbc, _('Export Address'))
            delivery_terms = etree.SubElement(
                delivery, '{%s}DeliveryTerms' % cac)
            if not self.invoice_incoterm_id:
                raise UserError(_("Export invoices require incoterms!"))
            etree.SubElement(delivery_terms, '{%s}ID' % cbc,
                             attrib={'schemeID': 'INCOTERMS'}).text = \
                self.invoice_incoterm_id.code
            etree.SubElement(delivery_terms, '{%s}SpecialTerms' % cbc).text = \
                self.invoice_incoterm_id.name
            shipment = etree.SubElement(delivery, '{%s}Shipment' % cac)
            etree.SubElement(shipment, '{%s}ID' % cbc)
            etree.SubElement(shipment, '{%s}DeclaredCustomsValueAmount' % cbc,
                             attrib={'currencyID':
                                         self.currency_id.name}).text = \
                '%.*f' % (price_precision, line_price_unit)
            goods = etree.SubElement(shipment, '{%s}GoodsItem' % cac)
            if not line.product_id.hs_code:
                raise UserError(_("Export product %s require hs code!") %
                                line.product_id.name)
            etree.SubElement(goods, '{%s}RequiredCustomsID' % cbc).text = \
                line.product_id.hs_code
            stage = etree.SubElement(shipment, '{%s}ShipmentStage' % cac)
            if not self.l10n_tr_transport_mode_code:
                raise UserError(_("Export invoice requires transport mode!"))
            etree.SubElement(stage, '{%s}TransportModeCode' % cbc).text = \
                self.l10n_tr_transport_mode_code
            handling = etree.SubElement(shipment, '{%s}TransportHandlingUnit'
                                        % cac)
            package = etree.SubElement(handling, '{%s}ActualPackage'
                                        % cac)
            etree.SubElement(package, '{%s}ID' % cbc).text = str(line.id)
            etree.SubElement(package, '{%s}Quantity' % cbc).text = \
                str(line.l10n_tr_package_quantity) or '0'
            if line.l10n_tr_package_type_id:
                if not line.l10n_tr_package_type_id.l10n_tr_unece_code:
                    raise UserError(_("Export invoice line %s requires package type code!")
                                    % line.name)
                etree.SubElement(package, '{%s}PackagingTypeCode' % cbc).text = \
                    line.l10n_tr_package_type_id.l10n_tr_unece_code

