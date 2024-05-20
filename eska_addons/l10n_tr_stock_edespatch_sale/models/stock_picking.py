# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from lxml import etree
from odoo import api, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def edespatch_generate_order_xml(self, parent, cac, cbc):
        if self.sale_id and self.sale_id.state in ['sale', 'done']:
            order = etree.SubElement(parent, '{%s}OrderReference' % cac)
            order_reference = self.sale_id.client_order_ref or self.sale_id.name
            etree.SubElement(order, '{%s}ID' % cbc).text = order_reference
            etree.SubElement(order, '{%s}IssueDate' % cbc).text = \
                self.sale_id.date_order.strftime("%Y-%m-%d")
        return super(StockPicking, self).edespatch_generate_order_xml(
            parent, cac, cbc)

    @api.model
    def edespatch_get_buyer(self):
        if self.sale_id and self.sale_id.state in ['sale', 'done']:
            return self.sale_id.partner_id.commercial_partner_id
        else:
            return super().edespatch_get_buyer()

    '''
    @api.model
    def edespatch_generate_order_line_xml(self, parent, cac, cbc, line):
        result = super(StockPicking, self).edespatch_generate_order_line_xml(
            parent, cac, cbc, line)
        if line.move_id.sale_line_id:
            line.move_id.sale_line_id.order_id.edespatch_generate_order_xml(
                parent, cac, cbc)
        return result
    '''