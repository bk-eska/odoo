# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey Tax Office',
    'summary': 'Türkiye Vergi Daireleri',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'data/account_tax_office_data.xml',
        'views/account_tax_office_view.xml',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'views/report_invoice.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
