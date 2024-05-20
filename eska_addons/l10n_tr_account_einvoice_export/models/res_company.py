# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from odoo import api, models


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model
    def einvoice_process_response(self, envelope_uuid, document, invoice, response, ns):
        result = super(ResCompany, self).einvoice_process_response(
            envelope_uuid, document, invoice, response, ns)
        profile = self.ubltr_get_field(document, ns, './cbc:ProfileID')
        response_code = self.ubltr_get_field(
            response, ns, './cac:Response/cbc:ResponseCode')
        description = self.ubltr_get_field(
            response, ns, './cac:Response/cbc:Description')
        if profile == 'IHRACAT' and response_code == 'KABUL':
            id_path = '//cac:SenderParty/cac:PartyIdentification/cbc:ID'
            ref_no = self.ubltr_get_field(
                document, ns, id_path + '[@schemeID="GTB_REFNO"]')
            tescil_no = self.ubltr_get_field(
                document, ns, id_path + '[@schemeID="GTB_GCB_TESCILNO"]')
            tarih = self.ubltr_get_field(
                document, ns, id_path + '[@schemeID="GTB_FIILI_IHRACAT_TARIHI"]')
            export_date = False
            if tarih:
                export_date = datetime.strptime(tarih, '%Y-%m-%d').date()
            invoice.write({
                'l10n_tr_einvoice_gtb_refno': ref_no,
                'l10n_tr_einvoice_gtb_gcb_tescilno': tescil_no,
                'l10n_tr_einvoice_gtb_export_date': export_date,
            })
            # intaç tarihine göre kur düzeltmeleri
            invoice.write({
                'date': export_date,
            })
        elif profile == 'YOLCUBERABERFATURA' and response_code == 'GUMRUKONAY':
            invoice.l10n_tr_einvoice_response_uuid = envelope_uuid
            invoice.action_einvoice_completed(description)
        return result
