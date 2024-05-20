# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Delivery With Fleet',
    'summary': 'Türkiye Teslimat Filo Köprü Modülü',
    'version': '16.0.1.0.0',
    'category': 'Localization',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'l10n_tr_delivery',
        'fleet',
    ],
    'data': [
        'views/stock_picking_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
