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




    """
    #check if the uploaded file is the correct format(.pdf) other wise raise an error (status code: 400)
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    try:

        file_content = await file.read()
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            if not pdf.pages:
                return JSONResponse(content={"filename": file.filename, "extracted_text": "no pages found in the pdf"}, status_code=200)

            extracted_text = ""
            for i in range(len(pdf.pages)):
                page = pdf.pages[i]
                extracted_text += page.extract_text() + "\n"

            return JSONResponse(content={"filename" : file.filename, "extracted_text": extracted_text}, status_code=200)

    except PDFSyntaxError:
        raise HTTPException(status_code=422, detail="unable to read pdf file. the pdf might be corrupted")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""







