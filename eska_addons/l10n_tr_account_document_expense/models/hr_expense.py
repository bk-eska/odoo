# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    def _prepare_move_vals(self):
        res = super(HrExpenseSheet, self)._prepare_move_vals()
        if self.company_id.l10n_tr_use_document:
            res.update({'l10n_tr_document_type': 'other',
                         'l10n_tr_document_type_description': _('Expense Form'),
                         'l10n_tr_document_number': 'MASRAF/%d' % self.id,
                         'l10n_tr_document_date': self.accounting_date})
        return res
