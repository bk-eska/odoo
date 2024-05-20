# Copyright 2024 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import requests
import logging

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(selection_add=[
        ('mng', "MNG Kargo")
    ], ondelete={'mng': lambda recs: recs.write({'delivery_type': 'fixed', 'fixed_price': 0})})

    mng_default_package_type_id = fields.Many2one(
        comodel_name='stock.package.type',
        string='MNG Package Type',
    )

    mng_api_key = fields.Char(
        string="MNG API Key",
        groups="base.group_system",
    )

    mng_secret = fields.Char(
        string="MNG Secret",
        groups="base.group_system",
    )

    mng_username = fields.Char(
        string="MNG Username",
        groups="base.group_system",
    )

    mng_password = fields.Char(
        string="MNG Password",
        groups="base.group_system",
    )

    mng_service_type = fields.Selection(
        string="MNG Service Type",
        selection=[
            ('1', 'STANDART_TESLİMAT'),
            ('7', 'GUNİCİ_TESLİMAT'),
            ('8', 'AKŞAM_TESLİMAT '),
        ],
        default='1',
    )

    mng_sms1 = fields.Boolean(
        string="SMS On Destination Branch",
        help="Send SMS to Recipient When Shipment Reached to Destination Branch",
    )

    mng_sms2 = fields.Boolean(
        string="SMS On Prepare",
        help="Send SMS to Recipient When Shipment First Prepare",
    )

    mng_sms3 = fields.Boolean(
        string="SMS On Delivery",
        help="Send SMS to Shipper When Shipment Delivered ",
    )

    mng_payment_type = fields.Selection(
        string="Payment Type",
        selection=[
            ('1', 'Sender'),
            ('2', 'Recipient'),
        ],
        required=True,
        default="1"
    )

    mng_pickup_type = fields.Selection(
        string="Pickup Type",
        selection=[
            ('1', 'Pickup from Address'),
            ('2', 'Bring to Branch'),
        ],
        required=True,
        default="1"
    )

    mng_delivery_type = fields.Selection(
        string="Delivery Type",
        selection=[
            ('1', 'Delivery To Address'),
            ('2', 'Call Recipient'),
        ],
        required=True,
        default="1"
    )

    mng_is_cod = fields.Boolean(
        string='Cash On Delivery',
    )

    def _compute_can_generate_return(self):
        super(DeliveryCarrier, self)._compute_can_generate_return()
        for carrier in self:
            if carrier.delivery_type == 'mng':
                carrier.can_generate_return = True

    def _mng_get_default_custom_package_code(self):
        return '3'

    def _mng_get_error_message(self, body):
        if 'moreInformation' in body:
            return body['moreInformation']
        elif 'title' in body:
            return body['title']
        elif 'error' in body and 'description' in body['error']:
            return body['error']['description']
        elif 'error' in body and 'Description' in body['error']:
            return body['error']['Description']
        elif 'errors' in body:
            return body['errors'][0]['description']
        else:
            return _('MNG Kargo Unknown Error')

    def _mng_get_url(self):
        prefix = 'api' if self.prod_environment else 'testapi'
        return 'https://%s.mngkargo.com.tr/mngapi/api/' % prefix

    def mng_get_token(self):
        url = self._mng_get_url() + 'token'
        headers = {
            'X-IBM-Client-Id': self.mng_api_key,
            'X-IBM-Client-Secret': self.mng_secret,
            "x-api-version": "1",
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        payload = {
            'customerNumber': self.mng_username,
            'password': self.mng_password,
            "identityType": "1",
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            body = response.json()
        except Exception as e:
            raise UserError(_("Token Error: ") + str(e))
        if response.status_code == 200:
            return body['jwt']
        else:
            raise UserError(_("Token Error: ") + self._mng_get_error_message(body))

    def mng_get_shipment_data(self, picking):
        url = self._mng_get_url() + 'standardqueryapi/getshipment/'
        headers = {
            'X-IBM-Client-Id': self.mng_api_key,
            'X-IBM-Client-Secret': self.mng_secret,
            "x-api-version": "1",
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        try:
            response = requests.get(url + str(picking.id), headers=headers)
        except Exception as e:
            raise UserError(_("Shipment Error: ") + str(e))
        body = response.json()
        if response.status_code == 200:
            return {
                'exact_price': body['shipment']['finalTotal'],
                'tracking_number': body['shipment']['shipmentNumber'],
            }
        else:
            raise UserError(_("Shipment Error: ") + self._mng_get_error_message(body))

    def _mng_convert_weight(self, weight):
        weight_uom_id = self.env['product.template']._get_weight_uom_id_from_ir_config_parameter()
        return weight_uom_id._compute_quantity(weight, self.env.ref('uom.product_uom_kgm'), round=False)
    def _mng_compute_items(self, packages):
        items = []
        sequence = 0
        for package in packages:
            sequence += 1
            weight_in_kg = self._mng_convert_weight(package.weight)
            name = package.order_id.name if package.order_id else package.picking_id.name
            desi = (package.dimension.get('length') *
                    package.dimension.get('width') *
                    package.dimension.get('height') / 3000)
            items.append({
                'barcode': name + ' ' + str(sequence),
                'kg': int(weight_in_kg),
                'desi': int(desi),
                'content': package.name,
            })
        return items

    def mng_rate_shipment(self, order):
        token = self.mng_get_token()
        url = self._mng_get_url() + 'standardqueryapi/calculate'

        packaging_type = self.mng_default_package_type_id.shipper_package_code
        packages = self._get_packages_from_order(order, self.mng_default_package_type_id)
        items = self._mng_compute_items(packages)
        if not order.partner_shipping_id.state_id:
            UserError(_("Send Shipping Error: State is missing on shipping address!"))

        payload = {
            "shipmentServiceType": int(self.mng_service_type),
            "packagingType": int(packaging_type),
            "paymentType": int(self.mng_payment_type),
            "pickupType": int(self.mng_pickup_type),
            "deliveryType": int(self.mng_delivery_type),
            "cityCode": 0,
            "districtCode": 0,
            "cityName": order.partner_shipping_id.state_id.name,
            "districtName": order.partner_shipping_id.city,
            "address": '%s %s' % (order.partner_shipping_id.street, order.partner_shipping_id.street2),
            "smsPreference1": 1 if self.mng_sms1 else 0,
            "smsPreference2": 1 if self.mng_sms2 else 0,
            "smsPreference3": 1 if self.mng_sms3 else 0,
            "orderPieceList": items,
        }

        headers = {
            'X-IBM-Client-Id': self.mng_api_key,
            'X-IBM-Client-Secret': self.mng_secret,
            "x-api-version": "1",
            "Authorization": "Bearer " + token,
            "content-type": "application/json",
            "accept": "application/json"
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            body = response.json()
        except Exception as e:
            return {'success': False,
                    'price': 0.0,
                    'error_message': _('Rate Error:\n%s', str(e)),
                    'warning_message': False}

        if response.status_code != 200:
            return {'success': False,
                    'price': 0.0,
                    'error_message': _('Rate Error:\n%s', self._mng_get_error_message(body)),
                    'warning_message': False}

        return {'success': True,
                'price': body['finalTotal'],
                'error_message': False,
                'warning_message': False}

    def mng_send_shipping(self, pickings):
        res = []
        token = self.mng_get_token()
        url = self._mng_get_url() + 'standardcmdapi/createOrder'
        for picking in pickings:
            headers = {
                'X-IBM-Client-Id': self.mng_api_key,
                'X-IBM-Client-Secret': self.mng_secret,
                "x-api-version": "1",
                "Authorization": "Bearer " + token,
                'accept': 'application/json',
                'content-type': 'application/json',
            }
            packages = self._get_packages_from_picking(
                picking, self.mng_default_package_type_id)
            items = self._mng_compute_items(packages)

            packaging_type = (picking.package_ids and
                              picking.package_ids[0].package_type_id.shipper_package_code or
                              self.mng_default_package_type_id.shipper_package_code)

            if not self.mng_is_cod:
                cod_amount = 0.0
            elif not picking.sale_id:
                UserError(_("Cash On Delivery is not possible without an order!"))
            else:
                cod_amount = self._compute_currency(
                    picking.sale_id,
                    picking.sale_id.amount_total,
                    'pricelist_to_company'
                )

            if not picking.partner_id.state_id:
                UserError(_("Send Shipping Error: State is missing on shipping address!"))

            payload = {
                "order": {
                    "referenceId": str(picking.id),
                    "barcode": picking.name,
                    "isCOD": 1 if self.mng_is_cod else 0,
                    "codAmount": cod_amount,
                    "shipmentServiceType": int(self.mng_service_type),
                    "packagingType": int(packaging_type),
                    "content": picking.name,
                    "smsPreference1": 1 if self.mng_sms1 else 0,
                    "smsPreference2": 1 if self.mng_sms2 else 0,
                    "smsPreference3": 1 if self.mng_sms3 else 0,
                    "paymentType": int(self.mng_payment_type),
                    "deliveryType": int(self.mng_delivery_type),
                    "description": picking.name,
                    "marketPlaceShortCode": "",
                    "marketPlaceSaleCode": "",
                },
                "orderPieceList": items,
                "recipient": {
                    "fullName": picking.partner_id.name,
                    "address": '%s %s' % (picking.partner_id.street,
                                      picking.partner_id.street2),
                    "cityCode": 0,
                    "districtCode": 0,
                    "cityName": picking.partner_id.state_id.name,
                    "districtName": picking.partner_id.city,
                    "bussinessPhoneNumber": picking.partner_id.phone,
                    "mobilePhoneNumber": picking.partner_id.mobile,
                },
            }

            try:
                response = requests.post(url, headers=headers, json=payload)
                body = response.json()
            except Exception as e:
                raise UserError(_("Send Shipping Error: ") + str(e))
            if response.status_code != 200:
                raise UserError(_("Send Shipping Error: ") + self._mng_get_error_message(body))

            res = res + [self.mng_get_shipment_data(picking)]

            if picking.carrier_id.return_label_on_delivery:
                self.get_return_label(picking)
        return res


    def mng_get_return_label(self, picking, tracking_number=None, origin_date=None):
        token = self.mng_get_token()
        url = self._mng_get_url() + 'standardcmdapi/createReturnOrder'
        headers = {
            'X-IBM-Client-Id': self.mng_api_key,
            'X-IBM-Client-Secret': self.mng_secret,
            "x-api-version": "1",
            "Authorization": "Bearer " + token,
            'accept': 'application/json',
            'content-type': 'application/json',
        }

        packages = self._get_packages_from_picking(
            picking, self.mng_default_package_type_id)
        items = self._mng_compute_items(packages)

        packaging_type = (picking.package_ids and
                          picking.package_ids[0].package_type_id.shipper_package_code or
                          self.mng_default_package_type_id.shipper_package_code)

        if not picking.partner_id.state_id:
            UserError(
                _("Send Shipping Error: State is missing on shipping address!"))

        payload = {
            "order": {
                "referenceId": str(picking.id),
                "barcode": picking.name,
                "shipmentServiceType": int(self.mng_service_type),
                "packagingType": int(packaging_type),
                "content": picking.name,
                "smsPreference1": 1 if self.mng_sms1 else 0,
                "smsPreference2": 1 if self.mng_sms2 else 0,
                "smsPreference3": 1 if self.mng_sms3 else 0,
                "paymentType": int(self.mng_payment_type),
                "deliveryType": int(self.mng_delivery_type),
                "description": picking.name,
            },
            "orderPieceList": items,
            "recipient": {
                "fullName": picking.partner_id.name,
                "address": '%s %s' % (picking.partner_id.street,
                                      picking.partner_id.street2),
                "cityCode": 0,
                "districtCode": 0,
                "cityName": picking.partner_id.state_id.name,
                "districtName": picking.partner_id.city,
                "bussinessPhoneNumber": picking.partner_id.phone,
                "mobilePhoneNumber": picking.partner_id.mobile,
            },
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            body = response.json()
        except Exception as e:
            raise UserError(_("Return Label Error: ") + str(e))
        if response.status_code != 200:
            raise UserError(_("Return Label Error: ") + self._mng_get_error_message(body))
        return self.mng_get_shipment_data(picking)

    def mng_get_tracking_link(self, picking):
        return 'https://www.mngkargo.com.tr/track/%s' % picking.carrier_tracking_ref

    def mng_cancel_shipment(self, pickings):
        token = self.mng_get_token()
        url = self._mng_get_url() + 'standardcmdapi/cancelorder/'
        headers = {
            'X-IBM-Client-Id': self.mng_api_key,
            'X-IBM-Client-Secret': self.mng_secret,
            "x-api-version": "1",
            "Authorization": "Bearer " + token,
            "accept": "application/json"
        }
        for picking in pickings:
            response = requests.put(url + picking.name, headers=headers)
            if response.status_code != 200:
                # body = response.json() TODO DEBUG
                #raise UserError(body.get('message'))
                raise UserError("Cannot cancel order %s" % picking.name)
