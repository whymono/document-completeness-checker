# this file is for the fastAPI entry point and not reserved for any logic

from fastapi import FastAPI, File, UploadFile, HTTPException
from core.extract_text import extract_text_from_pdf
from core.section import text_splitter
from core.embed import embed_text
import json

#initialize the fastAPI as app
app = FastAPI(title="DCC - Document Completeness Checker")

# returns a simple "statues ok" message when reached out to /health
@app.get("/health")
async def health_check():
    return {"status": "ok"}

#able to upload PDF when reached out to /upload-pdf
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # the function outputs either a str or an error code:-
    # str: perfect text
    # 1: the file type was improper (.pdf)
    # 2: no pages found
    # 3: syntax error
    # x: other error

    # use the extraxt text from PDF function from extract_text.py
    result = json.loads(extract_text_from_pdf(file).body.decode('utf-8'))
    newresult = embed_text(text_splitter(result["text"]))

    # see if the result has an error
    if "error" in result:
        if result["error"] == 1:
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
        elif result["error"] == 2:
            raise HTTPException(status_code=400, detail="No pages found in the PDF file.")
        elif result["error"] == 3:
            raise HTTPException(status_code=400, detail="Syntax error in the PDF file.")
        else:
            raise HTTPException(status_code=500, detail= result["error"])

    # if the result does not contain an error, push the result
    else:
        print(newresult)

