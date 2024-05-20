# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey MIS Builder Templates',
    'summary': 'Türkiye Muhasebe Raporları',
    'version': '16.0.1.0.0',
    'category': 'Localization',
    'author': 'ESKA',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'mis_builder',
    ],
    'data': [
        'data/mis_report_styles.xml',
        "data/mis_report_pl.xml",
        "data/mis_report_pl_simplified.xml",
        'data/mis_report_bs.xml',
    ],
    'installable': True,
    'auto_install': False,
}
