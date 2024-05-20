# Copyright 2023 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _
from odoo.exceptions import UserError


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    image_1920 = fields.Image(
        related='product_tmpl_id.image_1920',
    )

    is_bom_locked = fields.Boolean(
        string='Is Locked',
        readonly=True,
        copy=False,
    )

    def action_lock_bom(self):
        for rec in self:
            rec.write({'is_bom_locked': True})

    def action_unlock_bom(self):
        for rec in self:
            rec.with_context(bom_unlock=True).write({'is_bom_locked': False})

    def write(self, vals):
        for rec in self:
            if rec.is_bom_locked and not self.env.context.get('bom_unlock') :
                raise UserError(_('You are not allowed to update a locked BoM!'))
        return super(MrpBom, self).write(vals)
