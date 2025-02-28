{
    'name': 'Easy Invoice OCR',
    'depends': ['account'],
    'external_dependencies': {'python': ['easyocr', 'opencv-python', 'pdf2image']},
    'data': ['views/account_move_views.xml'],
    'installable': True,
}
