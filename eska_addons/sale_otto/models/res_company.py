# Copyright 2024 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

import requests
import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    def _get_default_otto_token_refresh(self):
        return datetime.now() - timedelta(minutes=30)

    otto_enabled = fields.Boolean(
        string="Otto",
    )

    otto_api_url = fields.Char(
        string='API URL',
        required=True,
        default='https://api.otto.market',
    )

    otto_username = fields.Char(
        string='Username',
        required=True,
    )

    otto_password = fields.Char(
        string='Password',
        required=True,
    )

    otto_token = fields.Char(
        string='Token',
    )

    otto_token_last_refresh = fields.Datetime(
        string='Last Token Refresh',
        default=_get_default_otto_token_refresh,
    )

    otto_last_so_check = fields.Datetime(
        string='Last SO Check',
    )

    @api.model
    def get_access_token(self):
        if self.otto_token_last_refresh <= (datetime.now() - timedelta(minutes=30)):
            try:
                response = requests.post(
                    url=f'{self.otto_api_url}/v1/token',
                    headers={
                        'Content-Type': 'application/x-www-form-urlencoded',
                        "cache-control": "no-cache",
                    },
                    data={
                        "grant_type": "password",
                        "client_id": "token-otto-api",
                        'username': self.otto_username,
                        'password': self.otto_password,
                    },
                )
                result = response.json()
            except Exception as e:
                _logger.error("Access Token Generation Error: " + str(e))
                raise UserError(_('Access Token Generation Error'))
            if response.status_code != 200:
                _logger.error("Access Token Generation Error: " + str(response.status_code))
                raise UserError(_('Access Token Generation Error: ' + str(response.status_code)))
            self.otto_token = '%s %s' % (result['token_type'], result['access_token'])
            self.otto_token_last_refresh = datetime.now()
        return self.otto_token

    def run_get_otto_orders(self):
        for comp in self.env['res.company'].search([]):
            if comp.otto_enabled:
                try:
                    comp.get_otto_orders()
                except Exception as e:
                    _logger.error("Get Orders Error: " + str(e))
                    raise UserError("Get Orders Error: " + str(e))
                comp.otto_last_so_check = datetime.today()

    def get_otto_orders(self):
        token = self.get_access_token()
        if not self.otto_last_so_check:
            modified_date_start = datetime.today().replace(month=1, day=1)
        else:
            modified_date_start = self.otto_last_so_check
        next = True
        next_url = ''
        while next:
            params = {
                'fulfillmentStatus': 'PROCESSABLE',
                'fromDate': modified_date_start.strftime('%Y-%m-%dT%H:%M:%SZ'),
            }
            if next_url:
                nextcursor = next_url.split('nextcursor=')[1].split('&limit=128')[0]
                params['nextcursor'] = nextcursor
            try:
                response = requests.get(
                    url=f'{self.otto_api_url}/v4/orders',
                    params=params,
                    headers={
                        'Authorization': token,
                    },
                )
                result = response.json()
            except Exception as e:
                _logger.error("Otto Get Order Error: " + str(e))
                raise UserError("Get Orders Error: " + str(e))
            if response.status_code != 200:
                _logger.error("Get Orders Error: " + str(response.status_code))
                raise UserError("Get Orders Error: " + str(response.status_code))

            if 'links' in result:
                links = result['links']
                if 'rel' in links[0] and links[0]['rel'] == 'next':
                    next_url = links[0]['href']
            else:
                next = False
                next_url = ''

            order_data = result['resources']
            for order in order_data:
                order_id = self.env['sale.order'].search([
                    ('otto_order_id', '=', order['salesOrderId']),
                ], limit=1)
                if order_id:
                    continue
                vals = {
                    'otto_order_id': order['salesOrderId'],
                    'origin': f"Otto Order {order['orderNumber']}",
                    'date_order': datetime.strptime(order['orderDate'][:-9], '%Y-%m-%dT%H:%M:%S'),
                }
                partner_id, partner_shipping_id = self._get_or_create_partners_from_data(order)
                vals['partner_id'] = partner_id.id
                vals['partner_shipping_id'] = partner_shipping_id.id
                order_line_values = self._get_order_values_from_data(order['positionItems'])
                if order_line_values:
                    vals['order_line'] = order_line_values
                if vals:
                    self.env['sale.order'].create(vals)

    def _get_or_create_partners_from_data(self, order):
        country_id = False
        buyer_address = order['invoiceAddress']
        buyer_address_name = f"{buyer_address.get('firstName', '')} {buyer_address.get('lastName', '')}"
        firstname = order['deliveryAddress'].get('firstName', '')
        lastname = order['deliveryAddress'].get('lastName', '')
        city = order['deliveryAddress'].get('city', '')
        country_code = order['deliveryAddress'].get('countryCode', '')
        street = order['deliveryAddress'].get('street', '')
        zip = order['deliveryAddress'].get('zipCode', '')
        email = order['deliveryAddress'].get('email', '')
        house_number = order['deliveryAddress'].get('houseNumber', '')
        phone = order['deliveryAddress'].get('phoneNumber', '')
        salutation = order['deliveryAddress'].get('salutation', '')
        is_company = salutation == 'COMPANY'

        shipping_address_name = f'{firstname} {lastname}'
        if country_code:
            country_id = self.env['res.country'].sudo().search([
                ('code', '=', country_code),
            ], limit=1)

        partner_vals = {
            'name': shipping_address_name,
            'street': street,
            'street2': house_number,
            'zip': zip,
            'city': city,
            'country_id': country_id.id,
            'phone': phone,
            'email': email,
        }
        contact = self.env['res.partner'].search([
            ('name', '=', buyer_address_name),
            ('is_company', '=', is_company),
            ('city', '=', city),
            ('street', '=', street),
            '|', ('email', '=', False), ('email', '=', email),
            '|', ('company_id', '=', False), ('company_id', '=', self.id),
        ], limit=1)
        if not contact:
            contact_name = buyer_address_name or f"Otto Customer # {order['orderNumber']}"
            contact = self.env['res.partner'].with_context(tracking_disable=True).create({
                'name': contact_name,
                'is_company': is_company,
                **partner_vals,
            })
        delivery = contact if (
                contact.name == shipping_address_name
                and contact.street == street
                and (not contact.street2 or contact.street2 == house_number)
                and contact.zip == zip
                and contact.city == city
                and contact.country_id.id == country_id.id
        ) else None
        if not delivery:
            delivery = self.env['res.partner'].search([
                ('parent_id', '=', contact.id),
                ('type', '=', 'delivery'),
                ('name', '=', shipping_address_name),
                ('street', '=', street),
                ('city', '=', city),
                ('country_id', '=', country_id.id),
                '|', ('company_id', '=', False), ('company_id', '=', self.id),
            ], limit=1)
        if not delivery:
            delivery = self.env['res.partner'].with_context(tracking_disable=True).create({
                'name': shipping_address_name,
                'type': 'delivery',
                'parent_id': contact.id,
                **partner_vals,
            })
        return contact, delivery

    def _get_order_values_from_data(self, items):
        line_vals = []
        for item in items:
            product_sku = item['product']['sku']
            product_name = item['product']['productTitle']
            product_id = self.env['product.product'].search([
                ('default_code', '=', product_sku),
                '|',
                ('product_tmpl_id.company_id', '=', False),
                ('product_tmpl_id.company_id', '=', self.id),
            ], limit=1)
            if not product_id:
                product_id = self.env.ref('sale_otto.default_otto_sale_product')
            product_tax_rate = item['product']['vatRate']
            tax_id = self.env['account.tax'].search([
                ('amount', '=', product_tax_rate),
                ('type_tax_use', '=', 'sale'),
                ('amount_type', '=', 'percent'),
                ('price_include', '=', True),
                ('company_id', '=', self.id),
            ], limit=1)
            price_unit = item['itemValueGrossPrice']['amount']
            line_vals.append((0, 0, {
                'product_id': product_id.id,
                'name': product_name,
                'product_uom': product_id.uom_id.id,
                'price_unit': price_unit,
                'product_uom_qty': 1,
                'tax_id': [(4, tax_id.id)] if tax_id else False,
            }))
        return line_vals
