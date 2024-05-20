# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Turkey - Account Sequence Numbers',
    'summary': 'Move Sequence Numbering in Turkey',
    'description': """
Turkey - Sequence Numbers
====================================================

This module adds sequence number to accounting entries, and a renumbering wizard.

Türk Ticaret Kanunu ve E-defter yönetmeliğine uygun olarak, muhasebe fişlerinde sıradan fiş numaraları
ve fişlerin içinde satır numaraları oluşturmayı sağlar.

(Giriş No = Yevmiye Sıra No = Fiş No = Madde No) (Öğe Sıra No = Satır No = Sıra No)
    """,
    'version': '16.0.1.0.0',
    'category': 'Localization',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account_fiscal_month',
    ],
    'data': [
        'wizard/date_range_renumber_view.xml',
        'security/ir.model.access.csv',
        'views/account_journal_view.xml',
        'views/account_move_view.xml',
        'views/date_range_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
