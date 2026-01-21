from pdfminer.pdfparser import PDFSyntaxError
import pdfplumber
from fastapi import UploadFile
from starlette.responses import JSONResponse


# this extracts the text from the PDF file
# in case of the provided file not being a .pdf, it will return 1 (indicates failure: invalid file type).
# in case of the provided file containing no pages, it will return 2 (indicates failure: no pages found).
# in case of Syntax error, it will return 3 (indicates failure: Syntax error)
# in case of other issues, it will return x (indicates failure: x)

# in case of success, it will return the extracted text (in the form of a string)
def extract_text_from_pdf(file: UploadFile) -> JSONResponse:
    if not file.filename.endswith('.pdf'):
        return JSONResponse(status_code=400, content={"error": 1})

    try:
        with pdfplumber.open(file.file) as pdf:
            if not pdf.pages:
                return JSONResponse(status_code=400, content={"error": 2})

            extracted_text = ""
            for page in pdf.pages:
                extracted_text += page.extract_text()  + "\\n"

            return JSONResponse(status_code=200, content={"filename": file.filename, "text": extracted_text})

    except PDFSyntaxError:
        return JSONResponse(status_code=422, content={"error": 3})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
