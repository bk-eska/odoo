# Copyright 2016 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.reports'

    route_ids = fields.One2many(
        comodel_name='ir.actions.reports.route',
        inverse_name='parent_id',
        string='Routes',
        help='A route is selected if there is no filter or the filter works '
             'for the records. If no route is works then it fallbacks '
             'to parent reports.',
    )

    def get_route(self, docids):
        if 'portal' in self.env.context and self.env.context.get('portal'):
            return False
        for route in self.route_ids:
            if self.model != route.filter_id.model_id:  # invalid route
                continue
            if route.filter_id:
                domain = [('id', 'in', docids)] + eval(
                    route.filter_id.domain)
                ctx = dict(self._context or {})
                ctx.update(eval(route.filter_id.context))
                record_ids = self.env[self.model].\
                    with_context(ctx).search(domain)
                if record_ids:
                    if len(record_ids) == len(docids):
                        return route
                    else:
                        raise ValidationError(
                            _('Records with different reports routes '
                              'cannot be printed together!'))
            else:
                return route
        return False

    def _render_qweb_html(self, report_ref, docids, data=None):
        report = self._get_report(report_ref)
        route = report.get_route(docids)
        if route:
            return self._render_qweb_html(route.report_id.report_name, docids, data)
        else:
            return super(IrActionsReport, self)._render_qweb_html(report_ref, docids, data)

    def _render_qweb_pdf(self, report_ref, res_ids, data=None):
        report = self._get_report(report_ref)
        route = report.get_route(res_ids)
        if route:
            return self._render_qweb_pdf(route.report_id.report_name, res_ids, data)
        else:
            return super(IrActionsReport, self)._render_qweb_pdf(report_ref, res_ids, data)

