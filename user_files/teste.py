import pdfkit
config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe") 
pdfkit.from_string('Hello!', 'out.pdf', configuration=config)
