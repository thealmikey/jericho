# src/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from pd_orchestra import PdOrchestra

app = FastAPI(title="Sound Orchestra MCP")

orchestra = PdOrchestra()  # one global instance

class StartProgress(BaseModel):
    task_name: str | None = None

class UpdateProgress(BaseModel):
    percent: float
    message: str | None = None

class FinishProgress(BaseModel):
    success: bool = True

class OneShot(BaseModel):
    cue: str
    file: str | None = None

@app.post("/start_progress_music")
async def start_progress_music(payload: StartProgress):
    orchestra.start_session(payload.task_name or "build")
    return {"status": "music started"}

@app.post("/update_progress")
async def update_progress(payload: UpdateProgress):
    if not 0 <= payload.percent <= 100:
        raise HTTPException(400, "percent must be 0-100")
    orchestra.update_progress(payload.percent, payload.message)
    return {"status": "progress updated"}

@app.post("/finish_progress")
async def finish_progress(payload: FinishProgress):
    orchestra.finish_session(success=payload.success)
    return {"status": "session finished"}

@app.post("/play_one_shot")
async def play_one_shot(payload: OneShot):
    orchestra.play_one_shot(payload.cue, payload.file)
    return {"status": "played"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=2424)