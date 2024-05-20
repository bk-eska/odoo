# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'utm.mixin']

    campaign_id = fields.Many2one(
        comodel_name='utm.campaign',
        string='Campaign',
        help="This is a name that helps you keep track of your different campaign efforts, e.g. Fall_Drive, Christmas_Special",
    )

    source_id = fields.Many2one(
        comodel_name='utm.source',
        string='Source',
        help="This is the source of the link, e.g. Search Engine, another domain, or name of email list",
    )

    medium_id = fields.Many2one(
        comodel_name='utm.medium',
        string='Medium',
        help="This is the method of delivery, e.g. Postcard, Email, or Banner Ad",
    )
