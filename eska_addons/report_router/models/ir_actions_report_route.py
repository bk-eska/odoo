# Copyright 2016 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class IrActionsReportRoute(models.Model):
    _name = 'ir.actions.reports.route'
    _description = 'Report Route'
    _order = 'sequence, id'

    parent_id = fields.Many2one(
        comodel_name='ir.actions.reports',
        string='Router',
        required=True,
        ondelete='cascade',
    )

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
    )

    report_id = fields.Many2one(
        comodel_name='ir.actions.reports',
        string='Report',
        required=True,
    )

    model = fields.Char(
        string="Model",
        related='parent_id.model'
    )

    filter_id = fields.Many2one(
        comodel_name='ir.filters',
        string='Filter',
    )

