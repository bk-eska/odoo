# Copyright 2021 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale Package Report Total Quantity',
    'summary': 'Adds total quantity to the packing list',
    'version': '16.0.1.0.0',
    'category': 'Stock',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale_package',
    ],
    'data': [
        "reports/report_packing_list.xml",
        "views/stock_quant_package_view.xml",
    ],
    'installable': True,
    'auto_install': False,
}
