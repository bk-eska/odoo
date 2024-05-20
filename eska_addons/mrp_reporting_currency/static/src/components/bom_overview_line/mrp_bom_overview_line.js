/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { formatMonetary } from "@web/views/fields/formatters";
import { BomOverviewLine } from "@mrp/components/bom_overview_line/mrp_bom_overview_line";

patch(BomOverviewLine.prototype, "mrp_reporting_currency", {
    setup() {
        this._super.apply();
        this.formatReportMonetary = (val) => formatMonetary(val, { currencyId: this.data.report_currency_id });
    },
});
