# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from collections import OrderedDict
from odoo.osv import expression

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

from odoo import http, _
from odoo.http import request


class CustomerLedgerPortal(CustomerPortal):

    @http.route(['/my/ledger', '/my/ledger/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_ledger(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        MoveLine = request.env['account.move.line']

        domain = [
            ('parent_state', 'not in', ('cancel', 'draft')),
            ('account_id.account_type', 'in', ('asset_receivable', 'liability_payable')),
            ('partner_id', 'child_of', partner.commercial_partner_id.id)
        ]

        _items_per_page = 100

        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'date'},
            'date_desc': {'label': _('Date DESC'), 'order': 'date desc'},
            'duedate': {'label': _('Due Date'), 'order': 'move_id.date_maturity desc'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'receivable': {'label': _('Receivable'), 'domain': [('account_id.account_type', '=', 'asset_receivable')]},
            'payable': {'label': _('Payable'), 'domain': [('account_id.account_type', '=', 'liability_payable')]},
        }

        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        line_count = MoveLine.sudo().search_count(domain)

        pager = portal_pager(
            url='/my/ledger',
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby},
            total=line_count,
            page=page,
            step=_items_per_page
        )

        lines = MoveLine.sudo().search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager['offset']
        )

        values.update({
            'date': date_begin,
            'ledger': lines,
            'page_name': 'ledger',
            'pager': pager,
            'default_url': '/my/ledger',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })

        return request.render("account_portal_partner_ledger.portal_my_ledger", values)
