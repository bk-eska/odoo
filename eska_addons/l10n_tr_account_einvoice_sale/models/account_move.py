# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import pytz
from lxml import etree

from odoo import api, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def einvoice_generate_order_xml(self, parent, cac, cbc):
        order_ids = self.mapped('invoice_line_ids.sale_line_ids.order_id')
        if len(order_ids) == 1:
            sale = order_ids[0]
            reference = etree.SubElement(parent, '{%s}OrderReference' % cac)
            order_reference = sale.client_order_ref or sale.name
            etree.SubElement(reference, '{%s}ID' % cbc).text = order_reference
            etree.SubElement(reference, '{%s}IssueDate' % cbc).text = \
                sale.date_order.replace(tzinfo=pytz.utc).astimezone(
                pytz.timezone('Europe/Istanbul')).strftime("%Y-%m-%d")

    @api.model
    def einvoice_buyer_party_xml(self, einvoice, cac, cbc, party):
        order_ids = self.mapped('invoice_line_ids.sale_line_ids.order_id')
        if len(order_ids) == 1:
            commercial_partner = order_ids[0].partner_id.commercial_partner_id
            customer = etree.SubElement(einvoice,
                                        '{%s}BuyerCustomerParty' % cac)
            commercial_partner.ubltr_generate_party_xml(
                'buyer', customer, cac, cbc, party.l10n_tr_party_identifiers)