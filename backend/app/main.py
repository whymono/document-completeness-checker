# this file is for the fastAPI entry point and not reserved for any logic
# trigger reload
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
import uuid
from fastapi.middleware.cors import CORSMiddleware
from app.core.extract_text import extract_text_from_pdf
from app.core.section import text_splitter
from app.core.embed import embed_text
from app.api.analyze import analyze_document
from app.core.config import settings
from app.core.logger import logger
from fastapi.responses import JSONResponse
import json

#initialize the fastAPI as app
app = FastAPI(title="DCC - Document Completeness Checker")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    logger.error(f"Unhandled server error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred on the server.", "error": str(exc)}
    )

# returns a simple "statues ok" message when reached out to /health
@app.get("/health")
async def health_check():
    return {"status": "ok"}

jobs = {}

def process_document(job_id: str, text: str):
    logger.info(f"Starting background job: {job_id}")
    try:
        logger.info(f"Job {job_id} - Splitting text")
        separated = text_splitter(text)
        
        logger.info(f"Job {job_id} - Embedding text")
        embedded = embed_text(separated)
        
        logger.info(f"Job {job_id} - Analyzing document")
        analysis = analyze_document(embedded=embedded, text=separated)
        
        analysis_json = json.loads(analysis)
        jobs[job_id] = {"status": "completed", "result": analysis_json}
        logger.info(f"Job {job_id} - Successfully completed")
    except json.JSONDecodeError as e:
        logger.error(f"Job {job_id} - Failed to decode JSON from LLM: {e}")
        jobs[job_id] = {"status": "failed", "error": "Failed to decode analysis JSON from the model."}
    except Exception as e:
        logger.error(f"Job {job_id} - Exception occurred: {e}", exc_info=True)
        jobs[job_id] = {"status": "failed", "error": str(e)}

@app.get("/job/{job_id}")
def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    # 1. Content Type Check
    if file.content_type and file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid content type. Only application/pdf is allowed.")

    # 2. Magic Number & Size Check
    magic_number = file.file.read(5)
    if magic_number != b"%PDF-":
         raise HTTPException(status_code=400, detail="Invalid file format. Not a true PDF document.")
    
    file_size = len(magic_number)
    chunk_size = 1024 * 1024
    
    while chunk := file.file.read(chunk_size):
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE:
             raise HTTPException(status_code=413, detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB.")
    
    # 3. Reset the file pointer for processing
    file.file.seek(0)

    # the function outputs either a str or an error code:-
    # str: perfect text
    # 1: the file type was improper (.pdf)
    # 2: no pages found
    # 3: syntax error
    # x: other error

    result = json.loads(extract_text_from_pdf(file).body.decode('utf-8'))
    # see if the result doesn't contain an error
    if not "error" in result:
        job_id = str(uuid.uuid4())
        jobs[job_id] = {"status": "processing"}
        background_tasks.add_task(process_document, job_id, result["text"])
        return {"job_id": job_id, "status": "processing"}

    # if the result does contain an error
    else:
        logger.warning(f"File upload error: code {result['error']}")
        if result["error"] == 1:
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
        elif result["error"] == 2:
            raise HTTPException(status_code=400, detail="No pages found in the PDF file.")
        elif result["error"] == 3:
            raise HTTPException(status_code=400, detail="Syntax error in the PDF file.")
        else:
            raise HTTPException(status_code=500, detail=result["error"])
