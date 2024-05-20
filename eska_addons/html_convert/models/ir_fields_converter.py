# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from lxml import html

from odoo import api, models


class IrFieldsConverter(models.AbstractModel):
    _inherit = "ir.fields.converter"

    @api.model
    def html_to_text(self, html_content):
        if not html_content or not html_content.strip():
            return ''
        doc = html.fromstring(html_content)
        return ''.join(line.strip()+"\n" for line in doc.xpath("//text()"))

    @api.model
    def html_to_string(self, html_content):
        if not html_content or not html_content.strip():
            return ''
        doc = html.fromstring(html_content)
        return ' '.join(line.strip() for line in doc.xpath("//text()"))
