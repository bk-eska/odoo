# Copyright 2018 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.tools import format_date


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_procurement_group_key(self):
        """Return a key with priority to be used to regroup lines in multiple
        procurement groups
        """
        priority = 24
        key = super()._get_procurement_group_key()
        # Check priority
        if key[0] < priority:
            if self.warehouse_id:
                # group by date instead of datetime
                return (priority, self.warehouse_id, key[1])
        return key
