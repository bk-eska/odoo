# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale Order Opportunity Required',
    'summary': 'Makes opportunity required on quotation and sale order',
    'version': '16.0.1.0.0',
    'category': 'CRM',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale_order_opportunity_visible',
    ],
    'data': [
        'views/sale_order_view.xml',
        'views/crm_team_views.xml',
    ],
    'installable': True,
}
