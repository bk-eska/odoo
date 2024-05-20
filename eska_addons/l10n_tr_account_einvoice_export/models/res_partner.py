# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from lxml import etree
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_tr_default_einvoice_profile = fields.Selection(
        selection_add=[
            ('IHRACAT', 'İhracat'),
            ('YOLCUBERABERFATURA', 'Yolcu Beraberinde Fatura'),
        ],
    )

    @api.model
    def ubltr_generate_passport(self, parent, cac, cbc):
        if not self.nationality_id:
            raise UserError(_("Customer doesn't have natioanality!"))
        etree.SubElement(parent, '{%s}NationalityID' % cbc).text \
            = self.nationality_id.code
        if not self.passport_ids:
            raise UserError(_("Customer doesn't have a passport!"))
        passport = etree.SubElement(parent, '{%s}IdentityDocumentReference' % cac)
        etree.SubElement(passport, '{%s}ID' % cbc).text \
            = self.passport_ids[0].name
        etree.SubElement(passport, '{%s}IssueDate' % cbc).text \
            = self.passport_ids[0].expire_date.strftime("%Y-%m-%d")
