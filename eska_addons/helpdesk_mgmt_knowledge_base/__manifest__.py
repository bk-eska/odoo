# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Helpdesk Management Knowledge Base',
    'summary': 'Helpdesk Management Knowledge Base',
    'version': '16.0.1.0.0',
    "category": "After-Sales",
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'LGPL-3',
    'depends': [
        'helpdesk_mgmt',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/helpdesk_ticket_views.xml',
        'views/helpdesk_ticket_knowledge_base.xml',
    ],
    'installable': True,
    'auto_install': False,
}
