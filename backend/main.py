from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import get_db_connection
from routes import task_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Database connection testing on application startup
    try:
        conn = get_db_connection()
        conn.close()
        print("Database connection tested successfully.")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise e
    yield


app = FastAPI(title="Task Manager API", lifespan=lifespan)

app.include_router(task_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok"}
