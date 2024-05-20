# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import models, fields

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    partner_assigned_id = fields.Many2one('res.partner', 'Assigned Partner')
