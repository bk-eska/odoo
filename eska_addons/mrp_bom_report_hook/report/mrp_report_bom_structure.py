# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, _
from odoo.addons.mrp.report.mrp_report_bom_structure import ReportBomStructure


class ReportBomStructureHook(models.AbstractModel):
    _inherit = 'reports.mrp.report_bom_structure'

    def get_bom_line_values(self, bom_line, line_visible):
        line_values = {
            'bom_id': bom_line['bom_id'],
            'name': bom_line['name'],
            'type': bom_line['type'],
            'quantity': bom_line['quantity'],
            'quantity_available': bom_line['quantity_available'],
            'quantity_on_hand': bom_line['quantity_on_hand'],
            'producible_qty': bom_line.get('producible_qty', False),
            'uom': bom_line['uom_name'],
            'prod_cost': bom_line['prod_cost'],
            'bom_cost': bom_line['bom_cost'],
            'route_name': bom_line['route_name'],
            'route_detail': bom_line['route_detail'],
            'lead_time': bom_line['lead_time'],
            'level': bom_line['level'],
            'code': bom_line['code'],
            'availability_state': bom_line['availability_state'],
            'availability_display': bom_line['availability_display'],
            'visible': line_visible,
            }
        return line_values

    def get_bom_operation_values(self, data, level, parent_unfolded):
        bom_operation_values = {
            'name': _('Operations'),
            'type': 'operation',
            'quantity': data['operations_time'],
            'uom': _('minutes'),
            'bom_cost': data['operations_cost'],
            'level': level,
            'visible': parent_unfolded,
        }
        return bom_operation_values

    def get_bom_operation_line_values(self, operation, level, operations_unfolded):
        bom_operation_line_values = {
            'name': operation['name'],
            'type': 'operation',
            'quantity': operation['quantity'],
            'uom': _('minutes'),
            'bom_cost': operation['bom_cost'],
            'level': level + 1,
            'visible': operations_unfolded,
        }
        return bom_operation_line_values

    def get_bom_byproduct_values(self, data, level, parent_unfolded):
        bom_byproduct_values = {
            'name': _('Byproducts'),
            'type': 'byproduct',
            'uom': False,
            'quantity': data['byproducts_total'],
            'bom_cost': data['byproducts_cost'],
            'level': level,
            'visible': parent_unfolded,
        }
        return bom_byproduct_values

    def get_bom_byproduct_line_values(self, byproduct, level, byproducts_unfolded):
        bom_byproduct_line_values = {
            'name': byproduct['name'],
            'type': 'byproduct',
            'quantity': byproduct['quantity'],
            'uom': byproduct['uom_name'],
            'prod_cost': byproduct['prod_cost'],
            'bom_cost': byproduct['bom_cost'],
            'level': level + 1,
            'visible': byproducts_unfolded,
        }
        return bom_byproduct_line_values

    def _register_hook(self):
        def _get_bom_array_lines(self, data, level, unfolded_ids, unfolded, parent_unfolded=True):
            bom_lines = data['components']
            lines = []
            for bom_line in bom_lines:
                line_unfolded = ('bom_' + str(bom_line['index'])) in unfolded_ids
                line_visible = level == 1 or unfolded or parent_unfolded
                lines.append(self.get_bom_line_values(bom_line, line_visible))
                if bom_line.get('components'):
                    lines += self._get_bom_array_lines(bom_line, level + 1, unfolded_ids, unfolded,
                                                       line_visible and line_unfolded)
            if data['operations']:
                lines.append(self.get_bom_operation_values(data, level, parent_unfolded))
                operations_unfolded = unfolded or (
                            parent_unfolded and ('operations_' + str(data['index'])) in unfolded_ids)
                for operation in data['operations']:
                    lines.append(self.get_bom_operation_line_values(operation, level, operations_unfolded))
            if data['byproducts']:
                lines.append(self.get_bom_byproduct_values(data, level, parent_unfolded))
                byproducts_unfolded = unfolded or (
                            parent_unfolded and ('byproducts_' + str(data['index'])) in unfolded_ids)
                for byproduct in data['byproducts']:
                    lines.append(self.get_bom_byproduct_line_values(byproduct, level, byproducts_unfolded))
            return lines
        ReportBomStructure._patch_method('_get_bom_array_lines', _get_bom_array_lines)
        return super(ReportBomStructureHook, self)._register_hook()
