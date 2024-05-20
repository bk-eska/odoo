# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'BA/BS Report',
    'summary': 'BA/BS Report',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'date_range_account',
        'report_xml',
        'report_xlsx',
        'l10n_tr_account_document',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/babs_wizard.xml',
        'reports/reports.xml',
        'views/menu.xml',
    ],
    'installable': True,
}