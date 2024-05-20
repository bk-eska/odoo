# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "CRM Final Customer",
    "version": "16.0.1.0.0",
    "summary": "Adding a final customer field to the CRM Opportunity",
    "description": "Adding a final customer field to the CRM Opportunity",
    "author": 'Eska',
    "website": 'http://www.eskayazilim.com.tr',
    "license": 'AGPL-3',
    "category": "CRM",
    "depends": [
        "sale_crm",
        "sale_final_customer",
    ],
    "data": [
        'views/crm_lead_views.xml',
    ],
    "installable": True,
}
