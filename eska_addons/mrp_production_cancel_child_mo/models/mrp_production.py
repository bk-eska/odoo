from odoo import models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def action_cancel(self):
        for mo in self:
            children = mo._get_children()
            children.action_cancel()
        return super().action_cancel()
