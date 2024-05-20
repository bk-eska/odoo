# -- coding: utf-8 --
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

from odoo import fields, models, api, _
import io
import base64
from odoo.tools.misc import xlsxwriter


class ProductDetailsWizard(models.TransientModel):
    _name = 'product.details.wizard'

    based_on = fields.Selection([
        ('products', 'Selected Products'),
        ('category', 'Product Category')
    ], required=True, default='products', string='Based On')

    category_id = fields.Many2one('product.category', string='Product Category')
    product_details_report = fields.Binary('Products')

    report_file = fields.Binary('File', readonly=True)
    xls_report_name = fields.Text(string='File Name')
    is_printed = fields.Boolean('Printed', default=False)

    def export_details(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'product.details.wizard'
        datas['form'] = self.read()[0]

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Sheet 1')
        worksheet.set_landscape()
        fl = self.based_on + '.xlsx'

        bold = workbook.add_format({'bold': True, 'align': 'center'})
        text = workbook.add_format({'font_size': 12, 'align': 'center'})
        if self.category_id:
            rec = self.env['product.product'].search([('categ_id', '=', self.category_id.id)])
        else:
            rec = self.env[context.get('active_model')].search([('id', 'in', datas['ids'])])
        print('rec', rec)
        worksheet.set_column(0, 2, 15)
        worksheet.set_column(3, 4, 25)
        worksheet.set_column(5, 7, 15)
        worksheet.set_column(8, 8, 25)
        worksheet.write(0, 0, 'ITEM', bold)
        worksheet.write(0, 1, 'ITEM CODE', bold)
        worksheet.write(0, 2, 'BARCODE', bold)
        worksheet.write(0, 3, 'DESCRIPTION', bold)
        worksheet.write(0, 4, 'UNIT OF MEASURE', bold)
        worksheet.write(0, 5, 'SIZE', bold)
        worksheet.write(0, 6, 'QTY', bold)
        worksheet.write(0, 7, 'SALE PRICE', bold)
        worksheet.write(0, 8, 'PICTURE', bold)

        row = 1
        col = 0
        row_num = 1
        print('product')
        for product in rec:
            print('product.default_code', product.default_code)
            worksheet.set_row(row_num, 98)
            worksheet.write(row, col, row_num, text)
            row_num = row_num + 1
            worksheet.write(row, col + 1, product.default_code, text)
            worksheet.write(row, col + 2, product.barcode, text)
            worksheet.write(row, col + 3, product.name, text)
            worksheet.write(row, col + 4, product.uom_id.name, text)
            worksheet.write(row, col + 5, product.standard_price, text)
            worksheet.write(row, col + 6, product.qty_available, text)
            worksheet.write(row, col + 7, product.list_price, text)
            if product.image_128:
                buf_image = io.BytesIO(base64.b64decode(product.image_128))
                worksheet.insert_image(row, col + 8, "product.png", {'image_data': buf_image})
            row = row + 1

        workbook.close()
        xlsx_data = output.getvalue()
        result = base64.encodebytes(xlsx_data)
        context = self.env.args
        ctx = dict(context[2])
        ctx.update({'report_file': result})
        ctx.update({'file': fl})

        self.xls_report_name = fl
        self.report_file = ctx['report_file']
        self.is_printed = True
        print('finalllyyy')
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.details.wizard',
            'target': 'new',
            'context': ctx,
            'res_id': self.id,
        }
