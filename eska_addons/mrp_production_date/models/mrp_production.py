# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    production_date = fields.Datetime(
        string='Production Date',
        help='This is the date on which the goods with this serial number were produced.',
    )

    def button_mark_done(self):
        res = super(MrpProduction, self).button_mark_done()
        for rec in self:
            if not rec.production_date:
                rec.production_date = fields.Datetime.now()
            if rec.product_id.tracking != 'none':
                rec.lot_producing_id.production_date = rec.production_date
        return res
