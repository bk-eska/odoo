# Copyright 2023 ESKA Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale CRM Delivery Date',
    'summary': 'To set an expected date for the sales order while creating opportunity in CRM.',
    'version': '16.0.1.0.0',
    'category': 'CRM',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'crm',
    ],
    'data': [
        "views/crm_lead_view.xml",
    ],
    'installable': True,
    'auto_install': False,
}
