# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import pytz
from lxml import etree

from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def einvoice_generate_order_xml(self, parent, cac, cbc):
        order_ids = self.mapped('invoice_line_ids.sale_line_ids.order_id')
        if len(order_ids) == 1:
            sale = order_ids[0]
            reference = etree.SubElement(parent, '{%s}OrderReference' % cac)
            order_reference = sale.client_order_ref or sale.name if self.l10n_tr_delivery_type == 'einvoice' else sale.name
            etree.SubElement(reference, '{%s}ID' % cbc).text = order_reference
            etree.SubElement(reference, '{%s}IssueDate' % cbc).text = \
                sale.date_order.replace(tzinfo=pytz.utc).astimezone(
                pytz.timezone('Europe/Istanbul')).strftime("%Y-%m-%d")
