from odoo import models, fields, api

class VendorBill(models.Model):
    _inherit = 'account.move'

    def auto_fill_from_ocr(self):
        # Fetch unprocessed OCR data and auto-fill the vendor bill
        invoice = self.env['invoice.ocr'].search([('is_processed', '=', True)], limit=1)
        if not invoice:
            raise ValueError("No processed OCR invoices available")

        data = self.env['invoice.parser'].parse_invoice(invoice.extracted_text)
        supplier = self.env['res.partner'].search([('name', '=', data['supplier_name'])], limit=1)

        if not supplier:
            supplier = self.env['res.partner'].create({'name': data['supplier_name']})

        self.write({
            'partner_id': supplier.id,
            'invoice_date': data['invoice_date'],
            'ref': data['invoice_number'],
            'amount_total': float(data['total_amount'].replace(',', '')),
        })

