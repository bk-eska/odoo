# Copyright 2023 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, _
from datetime import datetime


class ReportStockLedgerXlsx(models.AbstractModel):
    _name = 'reports.stock_ledger_report.stock_ledger_report_xlsx'
    _description = "Stock Ledger Report"
    _inherit = 'reports.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        worksheet = workbook.add_worksheet('Stock Ledger Report')
        location_id = data.get('location_id')
        start_date = data['start_date']
        end_date = data['end_date']
        show_price = data.get('show_price', False)

        style_header = workbook.add_format({'font_size': 12, 'border': True})
        style = workbook.add_format({'font_size': 12, 'bold': True})
        style_number = workbook.add_format({'align': 'right', 'font_size': 12, 'num_format': '0.00'})
        style_number2 = workbook.add_format({'align': 'right', 'font_size': 12, 'num_format': '0.0'})
        style_total = workbook.add_format({'align': 'right', 'font_size': 12, 'num_format': '0.0', 'border': True})
        style_total2 = workbook.add_format({'font_size': 12, 'bold': True, 'border': True})
        style_date = workbook.add_format({'align': 'left', 'font_size': 12, 'num_format': 'dd.mm.yyyy hh:mm:ss'})

        domain = [
            ('date', '>=', start_date),
            ('date', '<=', end_date),
            ('state', '=', 'done'),
        ]

        if location_id:
            domain += [
                "|",
                ('location_id', 'child_of', location_id),
                ("location_dest_id", 'child_of', location_id),
            ]
        else:
            domain += [
                "|",
                ('location_id.usage', '=', 'internal'),
                ("location_dest_id.usage", '=', 'internal'),
            ]

        if data['product_ids']:
            products = data['product_ids']
        else:
            products = self.env['stock.move'].search(domain).product_id.ids

        headers = [
            _("Description"),
            _("Reference"),
            _("Partner"),
            _("Origin"),
            _("Source Location"),
            _("Destination Location"),
            _("Date"),
            _("In/Qty"),
            _("Out/Qty"),
            _("Total/Qty"),

        ]

        if show_price:
            headers += [
                _("Price Unit"),
                _("Amount"),
                _("Remaining Amount"),
            ]

        for col_num, header in enumerate(headers):
            worksheet.write(9, col_num, header, style_header)

        row = 10
        total_quantity = 0.0
        total_remaining_amount = 0.0
        for product in products:
            for move in self.env['stock.move'].search(
                    domain + [(
                            'product_id', '=', product
                    )], order='date'):
                worksheet.set_column(0, 13, 20)
                worksheet.write(row, 0, move.product_id.name)
                if move.product_id.default_code:
                    worksheet.write(row, 1, move.product_id.default_code)
                else:
                    worksheet.write(row, 1, '')
                if move.partner_id:
                    worksheet.write(row, 2, move.partner_id.name)
                else:
                    worksheet.write(row, 2, '')
                if move.origin:
                    worksheet.write(row, 3, move.origin)
                else:
                    worksheet.write(row, 3, '')
                worksheet.write(row, 4, move.location_id.display_name)
                worksheet.write(row, 5, move.location_dest_id.display_name)
                worksheet.write(row, 6, move.date, style_date)
                if move.location_id.usage != 'internal' and move.location_dest_id.usage == 'internal':
                    in_qty = float(move.product_uom_qty)
                    worksheet.write(row, 7, in_qty, style_number2)
                    total_quantity += in_qty

                if move.location_id.usage == 'internal' and move.location_dest_id.usage != 'internal':
                    out_qty = float(move.product_uom_qty)
                    worksheet.write(row, 8, out_qty, style_number2)
                    total_quantity -= out_qty
                worksheet.write(row, 9, total_quantity, style_number)

                if show_price:
                    worksheet.write(row, 10, move.price_unit, style_number)
                    amount = float(round(sum(move.stock_valuation_layer_ids.mapped('value')), 2))
                    worksheet.write(row, 11, amount, style_number)
                    total_remaining_amount += sum(move.stock_valuation_layer_ids.mapped('value'))
                    worksheet.write(row, 12, float(round(total_remaining_amount, 2)), style_number)
                row += 1

        print_date = datetime.now()
        worksheet.write(4, 0, _("Print Date:"), style)
        worksheet.write(4, 1, print_date, style_date)

        date_range = f'{start_date} - {end_date}'
        worksheet.write(5, 0, _("Date:"), style)
        worksheet.write(5, 1, date_range, style_date)

        if location_id:
            location_name = self.env['stock.location'].browse(location_id).name
        else:
            location_name = _("All Locations")
        worksheet.merge_range(5, 4, 5, 5, _('Location: ') + location_name, style)

        total_in_qty = sum(
            move.product_uom_qty for move in self.env['stock.move'].search(domain + [('product_id', 'in', products)]) if
            move.location_id.usage != 'internal' and move.location_dest_id.usage == 'internal')
        total_out_qty = sum(
            move.product_uom_qty for move in self.env['stock.move'].search(domain + [('product_id', 'in', products)]) if
            move.location_id.usage == 'internal' and move.location_dest_id.usage != 'internal')

        amounts = [float(round(sum(move.stock_valuation_layer_ids.mapped('value')), 2)) for move in
                   self.env['stock.move'].search(domain + [('product_id', 'in', products)])]
        total_amount = sum(amounts)

        worksheet.write(row + 1, 6, _("Total:"), style_total2)
        worksheet.write(row + 1, 7, total_in_qty, style_total)
        worksheet.write(row + 1, 8, total_out_qty, style_total)
        if show_price:
            worksheet.write(row + 1, 9, '', style_total)
            worksheet.write(row + 1, 10, '', style_total)
            worksheet.write(row + 1, 11, total_amount, style_total)
