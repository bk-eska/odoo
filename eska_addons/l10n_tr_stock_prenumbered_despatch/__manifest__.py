# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Stock Pre-numbered Despatches',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Pre-numbered Despatches',
    'description': """
Pre-numbered Invoices
====================================================

Use pre-numbered despatch documents.

Numaralandırılmış irsaliye numaralarını kullanmanızı sağlar.
    """,
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'l10n_tr_stock_document',
    ],
    'data': [
        'views/stock_picking_type_view.xml',
        'views/stock_picking_view.xml',
    ],
    'installable': True,
}
