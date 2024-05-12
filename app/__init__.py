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
import concurrent.futures
import threading
import os
# Creating a lock
lock = threading.Lock()
from .helper import insert_text
import ocrmypdf
# Initialize Sanic application
app = Sanic("PDF_Processor")
session = Session(app, interface=InMemorySessionInterface())
jinja = SanicJinja2(app, session=session, pkg_name='app')

# Initialize PaddleOCR with the desired language(s)



def process_page(pdf, batch):
    ocr = PaddleOCR(lang="es", use_gpu=True, det=True, rec=True, cls=True, use_space_char=True, use_angle_cls=True, rec_algorithm='SVTR_LCNet')
    print(batch)
    for index in batch:
        with lock:
            page = pdf.get_page(index)
        image = page.render()
        np_image = image.to_numpy()
        output = ocr.ocr(np_image)
        print(f"page {index}")
        text_page = [[item[0][3], str(item[1][0]).lower(), item[0][0][1] - item[0][3][1]] for item in output[0] if item[1][1] > 0.5]
        for text in text_page:
            insert_text(self_pdf=page, pos_x=float(text[0][0]), pos_y=float(page.get_height()) - float(text[0][1]), 
                                text=text[1], font_size=abs(int(float(text[2]))))
        with lock:
            page.gen_content()
    return "Ok"

def create_batches(num_pages, num_batches):
    """Divide the range of pages into num_batches batches."""
    batch_size = max(num_pages // num_batches, 1)
    print(batch_size)
    batches = [list(range(i, min(i + batch_size, num_pages))) for i in range(0, num_pages, batch_size)]
    return batches

async def ocr_pdf(pdf_bytes):
    pdf = PdfDocument(io.BytesIO(pdf_bytes))
    output_stream = io.BytesIO()
    num_pages = len(pdf)
    num_workers = os.cpu_count()
    batches = create_batches(num_pages, num_workers)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_batch = {executor.submit(process_page, pdf, batch): batch for batch in batches}
        for future in concurrent.futures.as_completed(future_to_batch):
            batch_result = future.result()
            print(f"Processed batch with results: {batch_result}")  # Wait for all futures to complete
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
    processed_pdf = await ocr_pdf(file.body)
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
