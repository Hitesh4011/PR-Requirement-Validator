import sys
from fastapi import FastAPI

app = FastAPI(title="Task Manager API")

@app.get("/")
def health_check():
    return {"status": "ok"}
