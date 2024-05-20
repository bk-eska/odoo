# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import qrcode
import base64
from werkzeug import urls
from io import BytesIO
from odoo import fields, models
from odoo.addons.payment import utils as payment_utils


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_qr_code = fields.Binary(
        string="QR Code",
        compute="_generate_qr_code",
    )

    payment_link = fields.Char(
        string="Payment Link",
        compute='_compute_payment_link',
    )

    def _compute_payment_link(self):
        for rec in self:
            base_url = rec.get_base_url()
            url_params = {
                'reference': urls.url_quote(rec.name),
                'amount': self.amount_residual,
                'access_token': self._get_access_token(),
                **self._get_additional_link_values(),
            }
            rec.payment_link = f'{base_url}/payment/pay?{urls.url_encode(url_params)}'

    def _get_access_token(self):
        self.ensure_one()
        return payment_utils.generate_access_token(
            self.partner_id.id, self.amount_residual, self.currency_id.id
        )

    def _get_additional_link_values(self):
        self.ensure_one()
        return {
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
        }

    def _generate_qr_code(self, silent_errors=False):
        for record in self:
            if record.payment_link and record.state == 'posted':
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    border=4,
                )
                qr.add_data(self.payment_link)
                qr.make(fit=True)
                img = qr.make_image()
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                invoice_qr_code = base64.b64encode(buffered.getvalue())
                record.invoice_qr_code = invoice_qr_code
                silent_errors = silent_errors
            else:
                record.invoice_qr_code = False
