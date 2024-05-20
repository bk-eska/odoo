from odoo import models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _prepare_pdiff_aml_vals(self, qty, unit_valuation_difference):
        # don't create new move lines whatsoever if valuation is manual
        if (not self.company_id.anglo_saxon_accounting and
                self.product_id.categ_id.property_valuation == 'manual_periodic'):
            return []
        else:
            return super(qty, unit_valuation_difference)
