# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mail_limit = fields.Integer(
        config_parameter='mail_send_limit.mail_limit',
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['mail_limit'] = int(
            self.env['ir.config_parameter'].sudo().get_param(
                'mail_send_limit.mail_limit', default=1000)
        )
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param(
            'mail_send_limit.mail_limit', self.mail_limit
        )
        super(ResConfigSettings, self).set_values()
