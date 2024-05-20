# Copyright 2024 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    @http.route(auth="user")
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        return super(WebsiteSale, self).shop(
            page, category, search, ppg, **post)

    @http.route(auth="user")
    def product(self, product, category='', search='', **kwargs):
        return super(WebsiteSale, self).product(
            product, category, search, **kwargs)
