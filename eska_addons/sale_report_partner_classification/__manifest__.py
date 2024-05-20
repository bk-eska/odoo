# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale Report Partner Classification',
    'summary': 'Add partner classification to sale reports',
    'version': '16.0.1.0.0',
    'category': 'Sale',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'partner_classification',
    ],
    'data': [
        'reports/sale_report_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
