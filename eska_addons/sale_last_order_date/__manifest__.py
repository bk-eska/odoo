# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Last Order Date",
    "summary": "Computes the customer's last order date and adds it to contact tree view as an optional field.",
    "version": "16.0.1.0.0",
    "category": "Contacts",
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale',
    ],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
}
