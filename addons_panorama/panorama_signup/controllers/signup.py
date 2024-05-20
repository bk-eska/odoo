# Copyright 2024 ESKA (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.http import request
import base64

class WebAuthSignup(AuthSignupHome):
    """This class helps to set extra information in signup."""

    @http.route('/web/signup', type='http', auth='public', website=True,
                sitemap=False, csrf=False)
    def web_auth_signup(self, *args, **kw):
        """function used to add extra information at the time of signup"""
        res = super().web_auth_signup(*args, **kw)
        qcontext = self.get_auth_signup_qcontext()
        user = request.env['res.users']
        user_sudo = user.sudo().search(
            user._get_login_domain(qcontext.get('login')),
            order=user._get_login_order(), limit=1)
        if 'sales_permit_file' in kw:
            data_b64 = kw['sales_permit_file']
            data = base64.b64encode(data_b64.read()) if data_b64 else b''
            user_sudo.partner_id.commercial_partner_id.sales_permit_file = data
        if 'tobacco_license_file' in kw:
            data_b64 = kw['tobacco_license_file']
            data = base64.b64encode(data_b64.read()) if data_b64 else b''
            user_sudo.partner_id.commercial_partner_id.tobacco_license_file = data
        if 'phone' in kw:
            user_sudo.partner_id.commercial_partner_id.phone = kw['phone']
        if 'address' in kw:
            user_sudo.partner_id.commercial_partner_id.street = kw['address']
        if 'city' in kw:
            user_sudo.partner_id.commercial_partner_id.city = kw['city']
        if 'country' in kw:
            country = request.env['res.country'].search(
                [('id', '=', kw['country'])])
            user_sudo.partner_id.commercial_partner_id.country_id = country
        return res
