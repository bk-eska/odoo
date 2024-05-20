# Copyright 2024 ESKA (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, _


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.reports'

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        result = super()._render_qweb_pdf(report_ref, res_ids, data)

        report = self._get_report(report_ref)
        if report.model == 'mrp.production':
            for res_id in res_ids:
                production = self.env['mrp.production'].browse(res_id)
                production.report_printed = True
                production.message_post(body=_("%s çıktısı alındı.") % report.display_name)

        return result
