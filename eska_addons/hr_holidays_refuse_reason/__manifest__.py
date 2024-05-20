# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Leave Refuse Reason',
    'summary': 'Set a reason when refusing leave and notify followers',
    'version': '16.0.1.0.0',
    'category': 'Human Resources',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'hr_holidays',
    ],
    'data': [
        'wizard/hr_leave_refuse_reason_view.xml',
        'views/mail_templates.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
