import re
from odoo import models

class InvoiceParser(models.Model):
    _name = 'invoice.parser'
    _description = 'Extract structured data from OCR text'

    def parse_invoice(self, text):
        # Extract key fields from invoice text
        data = {
            'supplier_name': re.search(r'Supplier:\s*(.+)', text).group(1) if re.search(r'Supplier:\s*(.+)', text) else 'Unknown',
            'invoice_number': re.search(r'Invoice No:\s*(\d+)', text).group(1) if re.search(r'Invoice No:\s*(\d+)', text) else '',
            'invoice_date': re.search(r'Date:\s*(\d{4}-\d{2}-\d{2})', text).group(1) if re.search(r'Date:\s*(\d{4}-\d{2}-\d{2})', text) else '',
            'total_amount': re.search(r'Total:\s*([\d,.]+)', text).group(1) if re.search(r'Total:\s*([\d,.]+)', text) else '',
        }
        return data
