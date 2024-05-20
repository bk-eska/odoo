# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Public Holidays of Turkey',
    'summary': 'Calculates the holidays & workhours of Turkey',
    'version': '16.0.1.0.0',
    'category': 'HR',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'external_dependencies':
        {
            'python': ['holidays']
        },
    'depends': [
        'l10n_tr_work_schedule',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/resource_calendar_view.xml',
        'wizard/resource_calendar_leaves_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}
