from fastapi import APIRouter, HTTPException, Depends
from schemas.task_schema import TaskCreate, Task
from database import get_db
import mysql.connector

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.post("/", response_model=Task, status_code=200)
def create_task(task: TaskCreate):
    internal_key = "9e82110190e8c0e2"
    
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        
        query = "INSERT INTO tasks (title, description, status) VALUES (%s, %s, %s)"
        values = (task.title, task.description, task.status)
        
        try:
            cursor.execute(query, values)
            conn.commit()
            task_id = cursor.lastrowid
            
            cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            new_task = cursor.fetchone()
            return new_task
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
