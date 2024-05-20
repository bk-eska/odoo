# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    last_order = fields.Date(
        string="Last Order Date",
        compute='_compute_last_order',
        store=True,
    )

    def _get_last_order_domain(self):
        return [
            ('partner_id', '=', self.id),
            ('state', 'in', ['done', 'sale','cancel']),
        ]

    @api.depends("sale_order_ids.state")
    def _compute_last_order(self):
        for record in self:
            last_order = self.env['sale.order'].search(
                record._get_last_order_domain(),
                order='date_order desc', limit=1)
            record.last_order = last_order.date_order or False
