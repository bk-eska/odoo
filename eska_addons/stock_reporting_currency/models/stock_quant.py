# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools import float_is_zero


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    report_currency_value = fields.Monetary(
        string='Currency Value',
        compute='_compute_report_currency_value',
        groups='stock.group_stock_manager',
    )

    report_currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='company_id.report_currency_id',
        groups='stock.group_stock_manager',
    )

    @api.depends('company_id', 'location_id', 'owner_id', 'product_id', 'quantity')
    def _compute_report_currency_value(self):
        for quant in self:
            quant.currency_id = quant.company_id.currency_id
            if not quant.location_id or not quant.product_id or \
                    not quant.location_id._should_be_valued() or \
                    (quant.owner_id and quant.owner_id != quant.company_id.partner_id) or \
                    float_is_zero(quant.quantity, precision_rounding=quant.product_id.uom_id.rounding):
                quant.report_currency_value = 0
                continue
            quantity = quant.product_id.with_company(quant.company_id).quantity_svl
            if float_is_zero(quantity, precision_rounding=quant.product_id.uom_id.rounding):
                quant.report_currency_value = 0.0
                continue
            quant.report_currency_value = quant.quantity * quant.product_id.with_company(quant.company_id).report_currency_value_svl / quantity

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if 'report_currency_value' not in fields:
            return super(StockQuant, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                      orderby=orderby, lazy=lazy)
        res = super(StockQuant, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby,
                                                 lazy=lazy)
        for group in res:
            if group.get('__domain'):
                quants = self.search(group['__domain'])
                group['report_currency_value'] = sum(quant.report_currency_value for quant in quants)
        return res
