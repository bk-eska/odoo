# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'E-Fatura Stok',
    'summary': 'Türkiye E-Fatura Stok',
    'version': '16.0.2.0.0',
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'l10n_tr_account_einvoice',
        'l10n_tr_stock_document',
        'stock_picking_invoice_link',
    ],
    'data': [
        'views/account_move_view.xml'
    ],
    'installable': True,
    'auto_install': True,
}
