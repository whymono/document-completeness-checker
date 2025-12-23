# this file is for the fastAPI entry point and not reserved for any logic

from fastapi import FastAPI

#initialize the fastAPI as app
app = FastAPI(title="DCC - Document Completeness Checker")

# returns a simple message when reached out to
@app.get("/")
async def health_check():
    return {"status": "ok"}