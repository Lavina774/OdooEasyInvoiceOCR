import base64
import easyocr
import fitz  # PyMuPDF
from pdf2image import convert_from_bytes
from odoo import models

class OCREngine(models.Model):
    _name = 'ocr.engine'
    _description = 'OCR Engine for Invoice Processing'

    def extract_text(self, invoice):
        # Extract text from invoices using EasyOCR
        file_data = base64.b64decode(invoice.invoice_file)
        reader = easyocr.Reader(['en']) 

        if invoice.file_type == 'pdf':
            text = self.extract_text_from_pdf(file_data, reader)
        else:
            text = self.extract_text_from_image(file_data, reader)

        return text

    def extract_text_from_pdf(self, pdf_bytes, reader):
        # Automatically choose the best extracttion method
        text = self.extract_text_from_machine_pdf(pdf_bytes)
        if not text.strip():
            text = self.extract_text_from_scanned_pdf(pdf_bytes, reader)
        return text

    def extract_text_from_machine_pdf(self, pdf_bytes):
        # Extract text directly from machine-generated PDFs
        text = ""
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text("text") + "\n"
        return text

    def extract_text_from_scanned_pdf(self, pdf_bytes, reader):
        # Use EasyOCR to process scanned PDF
        images = convert_from_bytes(pdf_bytes)
        text = '\n'.join([self.extract_text_from_image(img, reader) for img in images])
        return text

    def extract_text_from_image(self, image_data, reader):
        # Use EasyOCR to extract text from images
        return '\n'.join(reader.readtext(image_data, detail=0))
