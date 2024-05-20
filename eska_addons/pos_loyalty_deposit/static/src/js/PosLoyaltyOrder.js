/** @odoo-module **/

import { Order } from 'point_of_sale.models';
import Registries from 'point_of_sale.Registries';

export const PosLoyaltyOrderDeposit = (Order) => class PosLoyaltyOrderDeposit extends Order {

    _getRewardLineValuesProduct(args) {
        const reward = args['reward'];
        if (reward.deposit) return []
        return super._getRewardLineValuesProduct(args);
    }

  _computeUnclaimedFreeProductQty(reward, coupon_id, product, remainingPoints) {
        if(reward.deposit){
          let claimed = 0;
          for (const line of this.get_orderlines()) {
            if (line.get_product().id === product.id) {
                claimed += line.get_quantity();
            }
          }
           return remainingPoints - claimed;
        }
        return super._computeUnclaimedFreeProductQty(reward, coupon_id, product, remainingPoints)
    }

    _computePotentialFreeProductQty(reward, product, remainingPoints) {
        if(reward.deposit){
          let claimed = 0;
          for (const line of this.get_orderlines()) {
            if (line.get_product().id === product.id) {
                claimed += line.get_quantity();
            }
          }
           return remainingPoints - claimed;
        }
        return super._computeUnclaimedFreeProductQty(reward, product, remainingPoints)
    }

}
Registries.Model.extend(Order, PosLoyaltyOrderDeposit);

