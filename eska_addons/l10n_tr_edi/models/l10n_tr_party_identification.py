# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class L10nTrPartyIdentification(models.Model):

    _name = 'l10n_tr.party.identification'
    _description = 'Partner Identification'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True,
    )

    side = fields.Selection(
        selection=[
            ('company', 'Company'),
            ('partner', 'Partner'),
        ],
        string='Side',
        required=True,
        default='company',
    )

    party_identification = fields.Selection(
        selection=[
            ('HIZMETNO', 'Hizmet No'),
            ('MUSTERINO', 'Müşteri No'),
            ('TESISATNO', 'Tesisat No'),
            ('TELEFONNO', 'Telefon No'),
            ('DISTRIBUTORNO', 'Distribütör No'),
            ('TICARETSICILNO', 'Ticaret Sicil No'),
            ('TAPDKNO', 'TAPDK No'),
            ('BAYINO', 'Bayi No'),
            ('ABONENO', 'Abone No'),
            ('ARACKIMLIKNO', 'Elektrikli Araç Kimlik No'),
            ('SAYACNO', 'Sayaç No'),
            ('URETICINO', 'Üretici No'),
            ('CIFTCINO', 'Çiftçi No'),
            ('IMALATCINO', 'İmalatçı No'),
            ('DOSYANO', 'Dosya No'),
            ('HASTANO', 'Hasta No'),
            ('MERSISNO', 'Mersis No'),
        ],
        string='Party Identification',
        required=True,
    )

    identifier = fields.Char(
        string='Identifier',
        required=True,
    )
