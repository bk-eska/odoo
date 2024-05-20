/** @odoo-module **/

import { RewardButton } from "@pos_loyalty/js/ControlButtons/RewardButton";
import Registries from 'point_of_sale.Registries';

export const RewardButtonDeposit = (RewardButton) => class RewardButtonDeposit extends RewardButton {

    async onClick() {
        const rewards = this._getPotentialRewards();
        if (rewards.length > 1) {
            const rewardsList = rewards.map((reward) => ({
                id: reward.reward.id,
                label: reward.reward.description,
                item: reward,
            }));
            rewardsList.unshift({
                id: 0,
                label: 'Apply All',
                item: false,
            })
            const { confirmed, payload: selectedReward } = await this.showPopup('SelectionPopup', {
                title: this.env._t('Please select a reward'),
                list: rewardsList,
            });
            if (confirmed) {
                if (!selectedReward) {
                    var result = false
                    for (const reward of rewardsList) {
                        if (reward.id) {
                            result = this._applyReward(reward.item.reward, reward.item.coupon_id, reward.item.potentialQty);
                        }
                    }
                    return result
                } else {
                    return this._applyReward(selectedReward.reward, selectedReward.coupon_id, selectedReward.potentialQty);
                }
            }
        } else {
            await super.onClick();
        }
    }

    async _applyReward(reward, coupon_id, potentialQty) {
         if (reward.reward_type == 'product' && reward.deposit) {
            for (var i = 0; i < potentialQty; i++) {
                this.trigger(
                'click-product',
                this.env.pos.db.get_product_by_id(reward.reward_product_ids[0])
                );
            }
            return true;
         }
         else
            return super._applyReward(reward, coupon_id, potentialQty);
    }

}
Registries.Component.extend(RewardButton, RewardButtonDeposit);

