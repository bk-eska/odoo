# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import pytz
from lxml import etree
from odoo import _, api, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def einvoice_generate_delivery_terms_xml(self, parent, cac, cbc):
        # this method will be used to export information as necessary
        return

    @api.model
    def einvoice_generate_shipment_xml(self, parent, cac, cbc, picking):
        shipment = etree.SubElement(parent, '{%s}Shipment' % cac)
        etree.SubElement(shipment, '{%s}ID' % cbc).text = picking.name
        uom_precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        uom_weight = self.env[
            'product.template']._get_weight_uom_id_from_ir_config_parameter()
        if picking.shipping_weight > 0:
            etree.SubElement(shipment, '{%s}GrossWeightMeasure' % cbc,
                             attrib={'unitCode': uom_weight.unece_code}).text = \
                '%.*f' % (uom_precision, picking.shipping_weight)
        if picking.weight > 0:
            etree.SubElement(shipment, '{%s}NetWeightMeasure' % cbc,
                             attrib={'unitCode': uom_weight.unece_code}).text = \
                str(picking.weight)
        if picking.l10n_tr_number_of_packages > 0:
            etree.SubElement(shipment,
                             '{%s}TotalTransportHandlingUnitQuantity' % cbc).text = \
                str(picking.l10n_tr_number_of_packages)
        return shipment

    @api.model
    def einvoice_generate_delivery_xml(self, parent, cac, cbc):
        pickings = self.l10n_tr_einvoice_despatch_ids or self.picking_ids.filtered(
            lambda p: p.l10n_tr_document_number and
                      p.picking_type_code == 'outgoing' and
                      p.state == 'done')
        for picking in pickings:
            delivery = etree.SubElement(parent, '{%s}Delivery' % cac)
            etree.SubElement(delivery, '{%s}ID' % cbc).text = picking.name
            if picking.carrier_tracking_ref:
                etree.SubElement(delivery, '{%s}TrackingID' % cbc).text = \
                    picking.carrier_tracking_ref
            address = etree.SubElement(delivery, '{%s}DeliveryAddress' % cac)
            picking.partner_id.ubltr_generate_address_xml(address, cac, cbc,
                                                          _('Delivery Address'))
            '''
            if picking.carrier_id:
                picking.carrier_id.partner_id.ubltr_generate_party_xml(
                    'carrier', delivery, cac, cbc)
            '''
            if picking.l10n_tr_date_despatch:
                despatch = etree.SubElement(delivery, '{%s}Despatch' % cac)
                l10n_tr_date_despatch = picking.l10n_tr_date_despatch.replace(
                    tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Istanbul'))
                despatch_date = l10n_tr_date_despatch.strftime("%Y-%m-%d")
                despatch_time = l10n_tr_date_despatch.strftime("%H:%M:%S")
                etree.SubElement(despatch, '{%s}ActualDespatchDate' % cbc).text = despatch_date
                etree.SubElement(despatch, '{%s}ActualDespatchTime' % cbc).text = despatch_time

            self.einvoice_generate_delivery_terms_xml(delivery, cac, cbc)
            self.einvoice_generate_shipment_xml(delivery, cac, cbc, picking)


