# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sales_permit_number = fields.Char(
        string='Sales Permit Number',
    )

    sales_permit_file = fields.Binary(
        string="Sales Permit File",
        attachment=True,
    )

    sales_permit_filename = fields.Char(
        string="Sales Permit Filename",
    )

    tobacco_license_number = fields.Char(
        string='Tobacco License Number',
    )

    tobacco_license_expiry_date = fields.Date(
        string='Tobacco License Expiry Date',
    )

    tobacco_license_file = fields.Binary(
        string="Tobacco License File",
        filename="tobacco_license_filename",
        attachment=True,
    )

    tobacco_license_filename = fields.Char(
        string="Tobacco License Filename",
    )

    excise_tax_number = fields.Char(
        string='Excise Tax Number',
    )

    excise_tax_expiry_date = fields.Date(
        string='Excise Tax Date',
    )

    excise_tax_file = fields.Binary(
        string="Tobacco License File",
        filename="excise_tax_filename",
        attachment=True,
    )

    excise_tax_filename = fields.Char(
        string="Tobacco License Filename",
    )