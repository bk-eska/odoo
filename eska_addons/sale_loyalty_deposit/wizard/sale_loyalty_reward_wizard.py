# Copyright 2023 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, _
from odoo.exceptions import ValidationError


class SaleLoyaltyRewardWizard(models.TransientModel):
    _inherit = 'sale.loyalty.reward.wizard'

    def action_apply_all(self):
        self.ensure_one()
        claimable_rewards = self.order_id._get_claimable_rewards()
        for reward_id in self.reward_ids:
            selected_product = reward_id.reward_product_ids[:1] if reward_id.reward_type == 'product' else False
            selected_coupon = False
            for coupon, rewards in claimable_rewards.items():
                if reward_id in rewards:
                    selected_coupon = coupon
                    break
            if not selected_coupon:
                raise ValidationError(
                    _('Coupon not found while trying to add the following reward: %s', reward_id.description))
            self.order_id._apply_program_reward(reward_id, coupon, product=selected_product)
            self.order_id._update_programs_and_rewards()

