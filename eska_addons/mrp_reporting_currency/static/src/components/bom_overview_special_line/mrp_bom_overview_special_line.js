/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { formatMonetary } from "@web/views/fields/formatters";
import { BomOverviewSpecialLine } from "@mrp/components/bom_overview_special_line/mrp_bom_overview_special_line";

patch(BomOverviewSpecialLine.prototype, "mrp_reporting_currency", {
    setup() {
        this._super.apply();
        this.formatReportMonetary = (val) => formatMonetary(val, { currencyId: this.data.report_currency_id });
    },
});