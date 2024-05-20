# Copyright 2016 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import io
from tempfile import NamedTemporaryFile

from lxml import etree

from PyPDF2 import PdfFileWriter, PdfFileReader

import base64

from odoo import _, fields, models, api
from odoo.exceptions import ValidationError


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.reports'

    xslt_transform = fields.Boolean(
        string="XSLT Transform",
        default=False,
    )

    xslt = fields.Binary(
        string='XSLT',
        copy=False,
        attachment=True,
    )

    attach_xml = fields.Boolean(
        string='Attach XML',
    )

    def attach_file_to_pdf(self, pdf, xml, filename):
        pdf_fd = PdfFileReader(io.BytesIO(pdf))
        new_fd = PdfFileWriter()
        new_fd.appendPagesFromReader(pdf_fd)
        new_fd.addAttachment(filename, xml)
        with NamedTemporaryFile(prefix='reports-xslt-', suffix='.pdf') as f:
            new_fd.write(f)
            f.seek(0)
            new_pdf = f.read()
            f.close()
        return new_pdf

    def _get_xslt_etree(self, report, doc, values=None):
        xslt_etree = values and values.get('xslt', False)
        if not xslt_etree:
            xslt_etree = etree.fromstring(base64.b64decode(report.xslt or ''))
            if getattr(doc, '_get_xslt_params', None):
                xslt_params = doc._get_xslt_params()
            else:
                raise ValidationError(_(
                    'This model does not support XSLT reports'))
            xmlns = 'http://www.w3.org/1999/XSL/Transform'
            for key, value in xslt_params.items():
                param = xslt_etree.find("{%s}param[@name='%s']" %
                                        (xmlns, key))
                if param is not None:
                    param.text = value
        return xslt_etree

    def _get_xml_etree(self, doc, values=None):
        xml_etree = values and values.get('xml', False)
        if not xml_etree:
            if getattr(doc, '_get_xml_etree', None):
                xml_etree = doc._get_xml_etree()
            else:
                raise ValidationError(_(
                    'This model does not support XSLT reports'))
        return xml_etree

    @api.model
    def _render_qweb_html(self, report_ref, docids, data=None):
        report = self._get_report(report_ref)
        if report.xslt_transform and len(docids) == 1:
            docs = self.env[report.model].browse(docids)
            xslt_etree = self._get_xslt_etree(report, docs[0], data)
            if data and data.get('get_xslt', False):
                return etree.tostring(xslt_etree), 'xslt'
            xslt = etree.XSLT(xslt_etree)
            return bytes(xslt(report._get_xml_etree(docs[0], data))), 'html'
        else:
            return super(IrActionsReport, self)._render_qweb_html(report_ref, docids, data)

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        report = self._get_report(report_ref)
        if report.xslt_transform and len(res_ids) == 1:
            html = self._render_qweb_html(report_ref, res_ids, data=data)[0]
            html = html.decode('utf-8')
            pdf = self.env['ir.actions.reports'].with_context(res_ids=False)._run_wkhtmltopdf([html])
            if report.attach_xml:
                docs = self.env[report.model].browse(res_ids)
                doc_id = docs[0]
                xml_filename = '%s.xml' % doc_id.name
                res_etree = report._get_xml_etree(doc_id, data)
                res_xml = etree.tostring(res_etree, pretty_print=True,
                                         encoding='utf-8')
                pdf = self.attach_file_to_pdf(pdf, res_xml, xml_filename)
            return pdf, 'pdf'
        else:
            return super(IrActionsReport, self)._render_qweb_pdf(
                report_ref, res_ids, data)
