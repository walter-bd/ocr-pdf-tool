import pypdfium2.raw as pdfium
import ctypes

def insert_text(self_pdf, text, pos_x, pos_y, font_size):
    """
    Insert text into the page at a specified position, using the writing system's ligature.
    This function supports Asian scripts such as Hindi.
    
    You may want to call :meth:`.generate_content` once you finished adding new content to the page.
    
    Parameters:
        text (str): The message to insert.
        pos_x (float): Distance from left border to first character.
        pos_y (float): Distance from bottom border to first character.
        font_size (float): Font size the text shall have.
    """
    # Load a standard font
    pdf_font = pdfium.FPDFText_LoadStandardFont(self_pdf.pdf.raw, "Arial".encode('utf-8'))
    
    start_point = pos_x
    # Create a text object
    pdf_textobj = pdfium.FPDFPageObj_CreateTextObj(self_pdf.pdf.raw, pdf_font, font_size)
    
    # Encode the entire string to UTF-16 and prepare it for ctypes
    utf16_text = text.encode('utf-16-le')
    # Ensure there's an even number of bytes for correct ushort processing
    if len(utf16_text) % 2 != 0:
        utf16_text += b'\x00'
    ushort_array = (ctypes.c_ushort * (len(utf16_text) // 2)).from_buffer_copy(utf16_text)

    pdfium.FPDFText_SetText(pdf_textobj, ushort_array)

    
    # Set text color to transparent (R, G, B, A)
    pdfium.FPDFPageObj_SetFillColor(pdf_textobj, 0, 0, 0, 0)  # Here, RGBA is 0, 0, 0, 0
    
    char_width = font_size * 0.5
    pdfium.FPDFPageObj_Transform(pdf_textobj, 1, 0, 0, 1, start_point, pos_y)
    
    # Insert the text object into the page
    pdfium.FPDFPage_InsertObject(self_pdf.raw, pdf_textobj)
    
    return self_pdf
