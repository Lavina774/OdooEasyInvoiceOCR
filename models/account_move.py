from odoo import models, fields, api
import easyocr
import cv2
import base64
import tempfile
import os
from pdf2image import convert_from_path
import numpy as np

class AccountMove(models.Model):
    _inherit = 'account.move'

    ocr_text = fields.Text(string="Extracted OCR Text")

    @api.model
    def _init_ocr(self):
        # Initialize EasyOCR for English and Portuguese, without GPU
        return easyocr.Reader(['en', 'pt'], gpu=False)

    def action_extract_ocr(self):
        # Check if there are any attachments
        if not self.attachment_ids:
            return self.message_post(body="No attachment found.")
        
        attachment = self.attachment_ids[0]
        reader = self._init_ocr()
        file_data = base64.b64decode(attachment.datas)
        file_extension = '.' + attachment.mimetype.split('/')[1].lower()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)

        try:
            with open(temp_file.name, 'wb') as f:
                f.write(file_data)
            text = self._process_file(temp_file.name, reader)
            self.ocr_text = text
            self.message_post(body=f"OCR Result:\n{text}")
        finally:
            os.unlink(temp_file.name)

    def _preprocess_image(self, image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply threshold to binarize
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        return thresh

    def _process_file(self, file_path, reader):
        # Determine file extension and process accordingly
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension in ['.jpg', '.jpeg', '.png']:
            image = cv2.imread(file_path)
        elif file_extension == '.pdf':
            images = convert_from_path(file_path, dpi=150)  # Reduced DPI for t2.micro performance
            image = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2BGR)  # First page
        else:
            return "Unsupported format. Use JPG, PNG, or PDF."

        # Preprocess the image
        processed_image = self._preprocess_image(image)

        # Extract text with EasyOCR
        results = reader.readtext(processed_image)

        # Format the extracted text
        text = "\n".join([f"Text: {res[1]} | Probability: {res[2]:.2f}" for res in results])
        return text if text else "No text detected."
