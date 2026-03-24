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


# returns a simple "statues ok" message when reached out to /health
@app.get("/health")
async def health_check():
    return {"status": "ok"}

jobs = {}

def process_document(job_id: str, text: str):
    try:
        separated = text_splitter(text)
        embedded = embed_text(separated)
        
        analysis = analyze_document(embedded=embedded, text=separated)
        print(analysis)
        
        analysis_json = json.loads(analysis)
        jobs[job_id] = {"status": "completed", "result": analysis_json}
    except json.JSONDecodeError:
        jobs[job_id] = {"status": "failed", "error": "Failed to decode analysis JSON from the model."}
    except Exception as e:
        jobs[job_id] = {"status": "failed", "error": str(e)}

@app.get("/job/{job_id}")
def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
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
        if result["error"] == 1:
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
        elif result["error"] == 2:
            raise HTTPException(status_code=400, detail="No pages found in the PDF file.")
        elif result["error"] == 3:
            raise HTTPException(status_code=400, detail="Syntax error in the PDF file.")
        else:
            raise HTTPException(status_code=500, detail= result["error"])
