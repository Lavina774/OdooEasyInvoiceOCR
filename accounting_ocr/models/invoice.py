import logging
import base64
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class InvoiceOCR(models.Model):
    _name = 'invoice.ocr'
    _description = 'OCR Invoice Processing'

    name = fields.Char(string="Invoice Name", required=True)
    invoice_file = fields.Binary(string="Upload Invoice File", required=True)
    file_type = fields.Selection([('image', 'Image'), ('pdf', 'PDF')], default='image')
    extracted_text = fields.Text(string="Extracted Text", readonly=True)
    is_processed = fields.Boolean(string="Processed", default=False)

    @api.model
    def create(self, vals):
        """Automatically process OCR when a new invoice is created"""
        record = super(InvoiceOCR, self).create(vals)
        if 'invoice_file' in vals and vals['invoice_file']:  
            record.process_invoice()
        return record

    def write(self, vals):
        """Automatically process OCR when an invoice file is updated"""
        result = super(InvoiceOCR, self).write(vals)
        if 'invoice_file' in vals and vals['invoice_file']: 
            self.process_invoice()
        return result

    def process_invoice(self):
        """Trigger OCR and text extraction"""
        self.ensure_one()
        if not self.invoice_file:
            return

        _logger.info(f"Processing OCR for invoice: {self.name}")
        self.extracted_text = self.env['ocr.engine'].extract_text(self)
        self.is_processed = bool(self.extracted_text)
        _logger.info(f"OCR Extracted Text for {self.name}: {self.extracted_text}")

    def do_close(self):
        return {'type': 'ir.actions.act_window_close'}


