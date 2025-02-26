{
    'name': 'Accounting OCR',
    'version': '17.0.1.1',
    'summary': 'Extract text from invoices using OCR',
    'category': 'Accounting',
    'author': 'Diverse Bytes',
    'License': 'LGPL-3',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/invoice_view.xml',
        'views/vendor_bill_view.xml',
        'data/cron_jobs.xml',
    ],
    'installable': True,
    'application': True,
}
