# Copyright 2023 Eska (https://eska.biz)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Pos Loyalty Deposit',
    'summary': 'Pos Loyalty Deposit ',
    'version': '16.0.1.0.0',
    'category': 'Sale',
    'author': 'Eska',
    'website': 'https://eska.biz',
    'license': 'AGPL-3',
    'depends': [
        'loyalty_deposit',
        'pos_loyalty',
    ],
    'data': [],
    'assets': {
        'point_of_sale.assets': [
            'pos_loyalty_deposit/static/src/js/*.js',
        ],
    },
    'installable': True,
    'auto_install': True,
}
