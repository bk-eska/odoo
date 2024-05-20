# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, _


class ReportBomStructure(models.AbstractModel):
    _inherit = 'reports.mrp.report_bom_structure'

    @api.model
    def _get_bom_data(self, bom, warehouse, product=False, line_qty=False, bom_line=False, level=0, parent_bom=False,
                      index=0, product_info=False, ignore_stock=False):
        bom_report_line = super(ReportBomStructure, self)._get_bom_data(
            bom, warehouse, product, line_qty, bom_line, level, parent_bom, index, product_info, ignore_stock)
        is_minimized = self.env.context.get('minimized', False)
        company = bom.company_id or self.env.company
        report_prod_cost = 0
        if not is_minimized:
            if product:
                report_prod_cost = product.uom_id._compute_price(
                    product.with_company(company).report_currency_standard_price,
                    bom.product_uom_id
                ) * bom_report_line['quantity']
            else:
                report_prod_cost = bom.product_tmpl_id.uom_id._compute_price(
                    bom.product_tmpl_id.with_company(company).report_currency_standard_price,
                    bom.product_uom_id
                ) * bom_report_line['quantity']

        bom_report_line['report_currency'] = company.report_currency_id
        bom_report_line['report_currency_id'] = company.report_currency_id.id
        bom_report_line['report_prod_cost'] = report_prod_cost
        bom_report_line['report_bom_cost'] = 0

        if not is_minimized:
            bom_report_line['report_operations_cost'] = sum(
                [op['report_bom_cost'] for op in bom_report_line['operations']])
            bom_report_line['report_bom_cost'] += bom_report_line['report_operations_cost']

            byproducts, byproduct_cost_portion = self._get_byproducts_lines(
                product, bom, bom_report_line['quantity'], level + 1, bom_report_line['report_bom_cost'], index)
            bom_report_line['report_byproducts_cost'] = sum(byproduct['report_bom_cost'] for byproduct in byproducts)
            bom_report_line['report_bom_cost'] *= bom_report_line['cost_share']

        for component in bom_report_line['components']:
            bom_report_line['report_bom_cost'] += component['report_bom_cost']

        return bom_report_line

    @api.model
    def _get_component_data(
            self, parent_bom, warehouse, bom_line, line_quantity, level, index, product_info, ignore_stock=False):
        res = super(ReportBomStructure, self)._get_component_data(
            parent_bom, warehouse, bom_line, line_quantity, level, index, product_info, ignore_stock)
        company = parent_bom.company_id or self.env.company
        report_price = bom_line.product_id.uom_id._compute_price(
            bom_line.product_id.with_company(company).report_currency_standard_price, bom_line.product_uom_id) * line_quantity
        rounded_report_price = company.report_currency_id.round(report_price)
        res['report_currency'] = company.report_currency_id
        res['report_currency_id'] = company.report_currency_id.id
        res['report_prod_cost'] = rounded_report_price
        res['report_bom_cost'] = rounded_report_price
        return res

    @api.model
    def _get_byproducts_lines(self, product, bom, bom_quantity, level, total, index):
        byproducts, byproduct_cost_portion = super(ReportBomStructure, self)._get_byproducts_lines(
            product, bom, bom_quantity, level, total, index)
        company = bom.company_id or self.env.company
        for byproduct in byproducts:
            bom_byproduct = bom.byproduct_ids.browse(byproduct['id'])
            line_quantity = (bom_quantity / (bom.product_qty or 1.0)) * bom_byproduct.product_qty
            price = bom_byproduct.product_id.uom_id._compute_price(
                bom_byproduct.product_id.with_company(company).report_currency_standard_price, bom_byproduct.product_uom_id) * line_quantity
            byproduct['report_currency_id'] = company.report_currency_id.id
            byproduct['report_prod_cost'] = company.report_currency_id.round(price)
            byproduct['report_bom_cost'] = company.report_currency_id.round(total * byproduct['cost_share'])
        return byproducts, byproduct_cost_portion

    @api.model
    def _get_operation_line(self, product, bom, qty, level, index):
        operations = super(ReportBomStructure, self)._get_operation_line(product, bom, qty, level, index)
        company = bom.company_id or self.env.company
        for operation in operations:
            total = ((operation['quantity'] / 60.0) * operation['operation'].workcenter_id.report_currency_costs_hour)
            operation['report_bom_cost'] = self.env.company.report_currency_id.round(total)
            operation['report_currency_id'] = company.report_currency_id.id
        return operations
    
    def get_bom_line_values(self, bom_line, line_visible):
        res = super(ReportBomStructure, self).get_bom_line_values(bom_line, line_visible)
        res['report_prod_cost'] = bom_line['report_prod_cost']
        res['report_bom_cost'] = bom_line['report_bom_cost']
        return res

    def get_bom_operation_values(self, data, level, parent_unfolded):
        res = super(ReportBomStructure, self).get_bom_operation_values(data, level, parent_unfolded)
        res['report_bom_cost'] = data['report_operations_cost']
        return res

    def get_bom_operation_line_values(self, operation, level, operations_unfolded):
        res = super(ReportBomStructure, self).get_bom_operation_line_values(operation, level, operations_unfolded)
        res['report_bom_cost'] = operation['report_bom_cost']
        return res

    def get_bom_byproduct_values(self, data, level, parent_unfolded):
        res = super(ReportBomStructure, self).get_bom_byproduct_values(data, level, parent_unfolded)
        res['report_bom_cost'] = data['report_byproducts_cost']
        return res

    def get_bom_byproduct_line_values(self, byproduct, level, byproducts_unfolded):
        res = super(ReportBomStructure, self).get_bom_byproduct_line_values( byproduct, level, byproducts_unfolded)
        res['report_bom_cost'] = byproduct['report_bom_cost']
        res['report_prod_cost'] = byproduct['report_prod_cost']
        return res
