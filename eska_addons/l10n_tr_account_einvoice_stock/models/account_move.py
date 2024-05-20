# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from lxml import etree
import pytz

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_tr_einvoice_despatch_ids = fields.Many2many(
        comodel_name='stock.picking',
        relation="l10n_tr_account_move_despatch_rel",
        string='Despatches',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    def einvoice_generate_despatch_xml(self, parent, cac, cbc):
        pickings = self.l10n_tr_einvoice_despatch_ids or self.picking_ids.filtered(
            lambda p: p.l10n_tr_document_number and
                      p.picking_type_code == 'outgoing' and
                      p.state == 'done')
        for picking in pickings:
            ref = etree.SubElement(parent, '{%s}DespatchDocumentReference' % cac)
            etree.SubElement(ref, '{%s}ID' % cbc).text = picking.l10n_tr_document_number
            issue_date = picking.l10n_tr_date_despatch or picking.date_done
            etree.SubElement(ref, '{%s}IssueDate' % cbc).text = issue_date.replace(
                tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Istanbul')).strftime("%Y-%m-%d")

