# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import threading
import logging

from odoo import api, models
from odoo.tools.safe_eval import datetime
from odoo.addons.mail.models.mail_mail import MailMail

_logger = logging.getLogger(__name__)


class MailMailHook(models.Model):
    _inherit = 'mail.mail'

    def _register_hook(self):
        @api.model
        def process_email_queue(self, ids=None):
            filters = ['&',
                       ('state', '=', 'outgoing'),
                       '|',
                       ('scheduled_date', '<', datetime.datetime.utcnow()),
                       ('scheduled_date', '=', False)]
            if 'filters' in self._context:
                filters.extend(self._context['filters'])

            limit = int(self.env['ir.config_parameter'].sudo().get_param(
                'mail_send_limit.mail_limit', default=1000))

            filtered_ids = self.search(filters, limit=limit).ids
            if not ids:
                ids = filtered_ids
            else:
                ids = list(set(filtered_ids) & set(ids))
            ids.sort()

            res = None
            try:
                # auto-commit except in testing mode
                auto_commit = not getattr(threading.currentThread(), 'testing', False)
                res = self.browse(ids).send(auto_commit=auto_commit)
            except Exception:
                _logger.exception("Failed processing mail queue")
            return res

        MailMail.process_email_queue = process_email_queue
        return super(MailMailHook, self)._register_hook()
