# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'E-Dönüşüm',
    'summary': 'Türkiye E-Dönüşüm Ortak Yapılarını içerir',
    'version': '16.0.1.0.0',
    'category': 'Base',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'l10n_tr_document',
        'l10n_tr_tax_office',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
