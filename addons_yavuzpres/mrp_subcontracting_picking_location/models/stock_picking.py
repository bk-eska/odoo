# Copyright 2024 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.depends('picking_type_id', 'partner_id')
    def _compute_location_id(self):
        super(StockPicking, self)._compute_location_id()
        for picking in self:
            picking = picking.with_company(picking.company_id)
            if picking.picking_type_id and picking.state == 'draft':
                if (picking.picking_type_id.subcontracting_operation and
                        picking.partner_id and picking.partner_id.property_stock_subcontractor):
                    if picking.picking_type_code == 'incoming':
                        picking.location_id = picking.partner_id.property_stock_subcontractor.id
                    elif picking.picking_type_code == 'outgoing':
                        picking.location_dest_id = picking.partner_id.property_stock_subcontractor.id
