# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Stock Document Fields',
    'summary': 'Türkiye Stok Belge Alanları',
    'version': '16.0.1.0.0',
    'category': 'Inventory',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'l10n_tr_document',
    ],
    'data': [
        'views/stock_move_view.xml',
        'views/stock_picking_type_view.xml',
        'views/stock_picking_view.xml',
    ],
    'auto_install': True,
    'external_dependencies': {
        'python': ['openupgradelib']
    },
    'pre_init_hook': 'pre_init_hook',
}
