# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_plan_procurement(self):
        self.ensure_one()
        treeview_ref = self.env.ref('sale_plan_procurement.view_order_line_tree_procurement')
        formview_ref = self.env.ref('sale_plan_procurement.view_order_line_form_procurement')
        action = {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'name': _('Sale Order Line'),
            'res_model': 'sale.order.line',
            'view_id': treeview_ref.id,
            'views': [(treeview_ref.id, 'tree'),
                      (formview_ref.id, 'form')],
            'domain': [('order_id', '=', self.id),
                       ('display_type', '=', False)],
            'context': {
                'default_order_id': self.id,
            },
        }
        return action

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for line in self.order_line:
            for purchase_line in line.purchase_line_ids:
                if purchase_line.planned_qty > 0.0:
                    purchase_line.product_qty = purchase_line.planned_qty
                else:
                    purchase_line.product_qty = 0.0
                    #purchase_line.unlink()
        po_ids = self.order_line.purchase_line_ids.mapped('order_id')
        for po in po_ids:
            if sum(po.order_line.mapped('product_qty')) > 0.0:
                po.button_confirm()
            else:
                po.button_cancel()
        return res
