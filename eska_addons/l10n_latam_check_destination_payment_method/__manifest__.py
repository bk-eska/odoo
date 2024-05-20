# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Latam Check Destination Payment Method',
    'summary': 'Latam Check Destination Payment Method',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'l10n_latam_check',
    ],
    'data': [
        'wizard/l10n_latam_payment_mass_transfer_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
