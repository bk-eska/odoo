# Copyright 2023 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale Loyalty Deposit',
    'summary': 'Loyalty Deposit ',
    'version': '16.0.1.0.0',
    'category': 'Sale',
    'author': 'Eska',
    'website': 'https://eska.biz',
    'license': 'AGPL-3',
    'depends': [
        'sale_loyalty',
        'loyalty_deposit',
    ],
    'data': [
        'wizard/sale_loyalty_reward_wizard_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
