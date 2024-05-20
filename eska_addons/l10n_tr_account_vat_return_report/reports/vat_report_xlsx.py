from odoo import models, _
import itertools


class ReportPurchaseVATPdf(models.AbstractModel):
    _name = 'reports.l10n_tr_account_vat_return_report.vat_report_xlsx'
    _description = "Account VAT Return Report"
    _inherit = 'reports.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('Account VAT Return Report')

        style_header = workbook.add_format({'font_size': 12, 'border': True, 'align': 'center', 'bold': True})
        style_order = workbook.add_format({'font_size': 12, 'border': True, 'align': 'center'})
        style = workbook.add_format({'font_size': 12, 'border': True})
        style_title = workbook.add_format({'font_size': 12, 'border': True, 'bold': True})
        style_number = workbook.add_format({'font_size': 12, 'num_format': '0.00'})
        style_date = workbook.add_format({'font_size': 12, 'num_format': 'dd.mm.yyyy', 'align': 'left'})
        style_total = workbook.add_format({'align': 'right', 'font_size': 12, 'num_format': '0.0', 'border': True})
        style_total2 = workbook.add_format({'font_size': 12, 'bold': True, 'border': True})

        date_range_id = data['date_range_id']
        date_range = self.env['date.range'].browse(date_range_id)
        date_start = date_range.date_start
        date_end = date_range.date_end

        purchase_invoices = self.env['account.move'].search([
            ('move_type', 'in', ['in_invoice', 'in_receipt']),
            ('state', 'in', ['posted', 'done']),
            ('invoice_date', '>=', date_start),
            ('invoice_date', '<=', date_end),
        ])

        headers = [
            'Sıra \n No',
            'Alış Faturasının \n Tarihi \n',
            'Alış Faturasının \n Serisi \n',
            'Alış Faturasının \n Sıra No’su \n',
            'Satıcının \n Adı-Soyadı / Ünvanı \n',
            'Satıcının \n Vergi Kimlik Numarası /\n TC Kimlik Numarası \n',
            'Alınan Mal ve/veya \n Hizmetin Cinsi \n',
            'Alınan Mal ve/veya \n Hizmetin Miktarı \n',
            'Alınan Mal ve/veya \n Hizmetin KDV \n Hariç Tutarı \n',
            'KDV’si \n',
            'GGB Tescil No’su \n (Alış İthalat İse) \n',
            'Belgenin İndirim \n Hakkının \n Kullanıldığı KDV \n Dönemi \n',
        ]

        row = 3
        col = 0
        for header in headers:
            sheet.write(row, col, header, style_header)
            sheet.set_column(col, col, 12)
            col += 1

        custom_text = "İNDİRİLECEK KDV LİSTESİ"
        sheet.write(1, 6, custom_text, style_title)

        rows = []
        counter = itertools.count(start=1)
        total_amount_untaxed = 0.0
        total_amount_tax = 0.0

        for invoice in purchase_invoices:
            tax_lines = invoice.line_ids.filtered(
                lambda l: l.tax_line_id.tax_group_id.l10n_tr_tax_type.code in ['0015', '9015'])
            amount_tax = sum(tax_lines.mapped('debit'))
            if amount_tax > 0.0:
                partner_name = invoice.partner_id.name or ''
                partner_vat = invoice.partner_id.vat or ''
                if partner_vat[:2] == 'TR':
                    partner_vat = partner_vat[2:]
                if invoice.l10n_tr_delivery_type == 'printed':
                    series = invoice.l10n_tr_document_number[0] if isinstance(
                        invoice.l10n_tr_document_number, str
                    ) and invoice.l10n_tr_document_number else ''
                    document_number = invoice.l10n_tr_document_number[1:] if isinstance(
                        invoice.l10n_tr_document_number, str) and len(invoice.l10n_tr_document_number
                                                                      ) > 1 else ''
                else:
                    series = ""
                    document_number = invoice.l10n_tr_document_number or ''
                tax_period = invoice.invoice_date.strftime('%Y%m')

                product_list = []
                for line in invoice.invoice_line_ids:
                    product_name = line.product_id.name or line.name or ''
                    product_list.append(product_name)
                product = '\n'.join(product_list)

                product_qty_list = []
                for line in invoice.invoice_line_ids:
                    uom_name = line.product_uom_id.name if line.product_uom_id.name else ''
                    product_qty_list.append(f"{line.quantity} {uom_name}")
                product_qty = '\n'.join(product_qty_list)

                amount_untaxed = abs(invoice.amount_untaxed_signed)

                rows.append((
                    next(counter),
                    invoice.invoice_date,
                    series,
                    document_number,
                    partner_name,
                    partner_vat,
                    product,
                    product_qty,
                    amount_untaxed,
                    amount_tax,
                    '',
                    tax_period,
                ))
                total_amount_untaxed += amount_untaxed
                total_amount_tax += amount_tax
        row = 4

        for row_data in rows:
            sheet.write(row, 0, row_data[0], style_order)
            sheet.write(row, 1, row_data[1], style_date)
            sheet.write(row, 2, row_data[2], style_order)
            sheet.write(row, 3, row_data[3], style)
            sheet.write(row, 4, row_data[4], style)
            sheet.write(row, 5, row_data[5], style)
            sheet.write(row, 6, row_data[6], style)
            sheet.write(row, 7, row_data[7], style)
            sheet.write(row, 8, row_data[8], style_number)
            sheet.write(row, 9, row_data[9], style_number)
            sheet.write(row, 10, row_data[10], style)
            sheet.write(row, 11, row_data[11], style_date)
            row += 1
        sheet.write(row, 7, _("Total:"), style_total2)
        sheet.write(row, 8, total_amount_untaxed, style_total)
        sheet.write(row, 9, total_amount_tax, style_total)
