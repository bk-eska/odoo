# Copyright 2021 Eska Technology LLC (www.eskaweb.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Collection',
    'summary': 'Collection App',
    'version': '16.0.2.0.0',
    'category': 'Accounting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'l10n_latam_check_destination_payment_method',
    ],
    'data': [
        'data/collection_order_sequence.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/collection_add_customer_wizard_view.xml',
        'wizard/collection_deposit_payment_wizard_view.xml',
        'wizard/collection_transfer_payment_wizard_view.xml',
        'views/collection_order_view.xml',
        'views/account_payment_view.xml',
        'views/account_journal_view.xml',
        'views/res_users_view.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
