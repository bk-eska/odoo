# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from zeep import Client

from odoo import fields, models, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    kimlik_cilt_no = fields.Char(
        string='Cilt No',
    )

    kimlik_kutuk_no = fields.Char(
        string='Kütük No',
    )

    kimlik_sayfa_no = fields.Char(
        string='Sayfa No',
    )

    kimlik_il = fields.Char(
        string='İl',
    )

    kimlik_ilce = fields.Char(
        string='İlçe',
    )

    kimlik_mahalle = fields.Char(
        string='Mahalle/Köy',
    )

    kimlik_seri_no = fields.Char(
        string='Seri No',
    )

    kimlik_verildigi_yer = fields.Char(
        string='Verildiği Yer',
    )

    kimlik_verildigi_tarih = fields.Date(
        string='Verildiği Tarih',
    )

    kimlik_tckn = fields.Char(
        string='TCKN',
    )

    yabanci_kimlik_no = fields.Char(
        string='Yabancı Kimlik No',
    )

    kimlik_turu = fields.Selection(
        selection=[
            ('TCKK', 'TC Çipli Kimlik Kartı'),
            ('TCNC', 'TC Nüfus Cüzdanı'),
            ('TCYK', 'TC Yabancı Kimlik Belgesi'),
            ('TCPC', 'TC Pasaportu'),
            ('TCSC', 'TC Sürücü Belgesi'),
        ],
        string='Kimlik türü',
    )

    nvi_validate = fields.Boolean(
        string='NVI Verified',
        readonly=True,
    )

    def write(self, vals):
        res = super().write(vals)
        if any(field in [
            'kimlik_turu', 'kimlik_tckn',
            'birth_date', 'name', 'yabanci_kimlik_no'
        ] for field in vals):
            self.nvi_validate = False
        return res

    def action_nvi_validate(self):
        for rec in self:
            if rec.kimlik_turu in ['TCKK', 'TCNC', 'TCSC']:
                if not rec.kimlik_tckn:
                    raise ValidationError(_('TCKN not found!'))
                number = rec.kimlik_tckn
                wsdl_url = "https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL"
            elif rec.kimlik_turu in ['TCYK', 'TCPC']:
                if not rec.yabanci_kimlik_no:
                    raise ValidationError(_('Yabancı kimlik no not found!'))
                number = rec.yabanci_kimlik_no
                wsdl_url = "https://tckimlik.nvi.gov.tr/Service/KPSPublicYabanciDogrula.asmx?WSDL"
            else:
                raise ValidationError(_('Validation type not found!'))
            names = rec.name.split()
            if len(names) < 2:
                raise ValidationError(_('Name error! Name must be 2 words!'))
            lastname = names.pop()
            firstname = ' '.join(names)

            client = Client(wsdl=wsdl_url)
            try:
                if rec.kimlik_turu in ['TCKK', 'TCNC', 'TCSC']:
                    response = client.service.TCKimlikNoDogrula(
                        TCKimlikNo=number,
                        Ad=firstname,
                        Soyad=lastname,
                        DogumYili=rec.birth_date.year
                    )
                else:
                    response = client.service.YabanciKimlikNoDogrula(
                        TCKimlikNo=number,
                        Ad=firstname,
                        Soyad=lastname,
                        DogumGun=rec.birth_date.day,
                        DogumAy=rec.birth_date.month,
                        DogumYil=rec.birth_date.year
                    )
            except Exception as e:
                _logger.error("Error: " + str(e))
                raise ValidationError(_("NVI Dogrulama Hatasi: " + str(e)))
            if response:
                _logger.info('Result: True')
                rec.nvi_validate = True
            else:
                _logger.error("Result: Verification Failed")
                raise ValidationError(_("Result: Verification Failed!"))
