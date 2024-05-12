import io
import numpy as np
from pdf2image import convert_from_bytes
from paddleocr import PaddleOCR
from reportlab.pdfgen import canvas
import img2pdf
import pytesseract
from sanic import Sanic, response
from sanic_jinja2 import SanicJinja2
from sanic_session import Session, InMemorySessionInterface
from pypdfium2 import PdfPage
import concurrent.futures
from pypdfium2 import PdfDocument
import pypdfium2 as pdfium
from .helper import insert_text
import ocrmypdf
# Initialize Sanic application
app = Sanic("PDF_Processor")
session = Session(app, interface=InMemorySessionInterface())
jinja = SanicJinja2(app, session=session, pkg_name='app')

# Initialize PaddleOCR with the desired language(s)
ocr = PaddleOCR(lang="es", use_gpu=True, det=True, rec=True, cls=True, use_space_char=True, use_angle_cls=True, rec_algorithm='SVTR_LCNet')





def ocr_pdf(pdf_bytes):
    pdf = PdfDocument(io.BytesIO(pdf_bytes))
    output_stream = io.BytesIO()
    for i, page in enumerate(pdf):
        image = page.render()
        np_image = image.to_numpy()
        output = ocr.ocr(np_image)
        print(f"page {i} output {output[0]}")
        text_page = [[item[0][3], str(item[1][0]).lower(), item[0][0][1] - item[0][3][1]] for item in output[0] if item[1][1] > 0.5]
        for text in text_page:
            insert_text(self_pdf=page, pos_x=float(text[0][0]), pos_y=float(page.get_height()) - float(text[0][1]), 
                             text=text[1], font_size=abs(int(float(text[2]))))
        page.gen_content()
    pdf.save(output_stream)
    output_stream.seek(0)
    return output_stream

@app.post('/process-pdf')
async def process_pdf(request):
    file = request.files.get('file')
    if not file:
        return response.text('No file uploaded', status=400)
    if not file.name.endswith('.pdf'):
        return response.text('Only PDF files are allowed', status=400)
    processed_pdf = ocr_pdf(file.body)
    # Create a response returning the PDF data
    return response.raw(
        body=processed_pdf.read(),
        headers={
            "Content-Type": "application/pdf",
            "Content-Disposition": 'attachment; filename="downloaded.pdf"'
        }
    )

@app.get("/")
async def index(request):
    return jinja.render('index.html', request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
