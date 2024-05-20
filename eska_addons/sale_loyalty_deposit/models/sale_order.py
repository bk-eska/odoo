# Copyright 2023 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import random

from odoo import models, _
from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.tools.float_utils import float_round


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_reward_values_product(self, reward, coupon, product=None, **kwargs):
        result = super(SaleOrder, self)._get_reward_values_product(reward, coupon, **kwargs)
        if reward.deposit:
            reward_products = reward.reward_product_id + reward.reward_product_tag_id.product_ids
            product = product or reward_products[:1]
            result[0].update({
                'name': _("Deposit Product - %(product)s", product=product.name),
                'price_unit': product.lst_price,
                'discount': 0.0,
            })
        return result

