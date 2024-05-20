# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, _


class BABSReport(models.AbstractModel):
    _name = "reports.l10n_tr_account_babs_report.report_babs"
    _description = "BA BS Report"

    def _get_report_values(self, docids, data):
        wizard_id = data["wizard_id"]
        company_id = self.env["res.company"].browse(data["company_id"])
        date_range_id = self.env["date.range"].browse(data["date_range_id"])
        date_from = data["date_from"]
        date_to = data["date_to"]
        threshold = data["threshold"]
        declaration_type = data["declaration_type"]
        only_posted_moves = data["only_posted_moves"]
        title_prefix = _('Period') + ' %s : ' % date_range_id.name
        title_short_prefix = date_range_id.name

        domain = [
            ('company_id', '=', company_id.id),
            ("date", ">=", date_from),
            ("date", "<=", date_to),
            ("move_id.l10n_tr_delivery_type", "=", 'printed'),
            ('account_id.account_type', 'in', ['income', 'expense']),
        ]

        if only_posted_moves:
            domain += [('parent_state', '=', 'posted')]

        report_bs = {
            'journal_type': ('sale'),
            'title': title_prefix + _('Sale Declaration'),
            'title_short': title_short_prefix + ', ' + _('BS')}
        report_ba = {
            'journal_type': ('purchase'),
            'title': title_prefix + _('Purchase Declaration'),
            'title_short': title_short_prefix + ', ' + _('BA')}

        if declaration_type == 'sale':
            reports = [report_bs]
        elif declaration_type == 'purchase':
            reports = [report_ba]
        else:
            reports = [report_bs, report_ba]

        for report in reports:
            if report['journal_type'] == 'sale':
                move_lines = self.env['account.move.line'].search(domain + [('journal_id.type', '=', 'sale')])
            elif report['journal_type'] == 'purchase':
                move_lines = self.env['account.move.line'].search(domain + [('journal_id.type', '=', 'purchase')])
            else:
                move_lines = self.env['account.move.line'].search(domain + [('journal_id.type', 'in', ['sale','purchase'])])
            partners = []
            total_sum_amount_untaxed = 0.0
            for partner in move_lines.mapped('partner_id'):
                p = {}
                partner_move_lines = move_lines.filtered(lambda l: l.partner_id == partner)
                sum_amount_untaxed = abs(sum(partner_move_lines.mapped('debit')) + sum(partner_move_lines.mapped('credit')))
                country_id = partner.country_id or False
                vat = partner.vat or ''
                country_name = ''
                tax_id = ''
                national_id = ''
                if country_id:
                    if country_id.code != 'TR':
                        if report['journal_type'] in ['sale']:
                            tax_id = '2222222222'
                        elif report['journal_type'] in ['purchase']:
                            tax_id = '1111111111'
                    elif len(vat) == 12:  # vkn
                        tax_id = vat[2:]
                    elif len(vat) == 13:  # tckno
                        national_id = vat[2:]
                else:
                    tax_id = vat[2:]
                p.update({
                    'partner_id': partner.id,
                    'partner_name': partner.name,
                    'amount_untaxed': sum_amount_untaxed,
                    'tax_id': tax_id,
                    'national_id': national_id,
                    'country_name': country_name,
                    'count': len(partner_move_lines),
                })
                if sum_amount_untaxed >= threshold:
                    total_sum_amount_untaxed += sum_amount_untaxed
                    partners.append(p)
            report.update({'partners': partners})
            report.update({'amount_untaxed': total_sum_amount_untaxed})

        return {
            "doc_ids": [wizard_id],
            "doc_model": "babs.reports.wizard",
            "docs": self.env["babs.reports.wizard"].browse(wizard_id),
            "company_name": company_id.name,
            "currency_name": company_id.currency_id.name,
            "reports": reports,
            "declaration_type": declaration_type,
            "only_posted_moves": only_posted_moves,
        }