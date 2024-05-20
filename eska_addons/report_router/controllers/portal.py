# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class PortalContract(CustomerPortal):

    def _show_report(self, model, report_type, report_ref, download=False):
        if download != 'true':
            context = request.env.context.copy()
            context.update({'portal': True})
            request.env.context = context
        return super()._show_report(model, report_type, report_ref, download)
