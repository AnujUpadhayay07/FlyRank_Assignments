from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from database import engine, create_db
from models import Task

app = FastAPI()


# ----------------------------
# Create database on startup
# ----------------------------
@app.on_event("startup")
def startup():
    create_db()

    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()

        if len(tasks) == 0:
            session.add(Task(title="Learn FastAPI"))
            session.add(Task(title="Build CRUD API"))
            session.add(Task(title="Push to GitHub", done=True))
            session.commit()


# ----------------------------
# Request Models
# ----------------------------
class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool


# ----------------------------
# Root Endpoint
# ----------------------------
@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "2.0",
        "endpoints": ["/tasks"]
    }


# ----------------------------
# Health Check
# ----------------------------
@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# ----------------------------
# Get All Tasks
# ----------------------------
@app.get("/tasks")
def get_tasks():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks


# ----------------------------
# Get Task By ID
# ----------------------------
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)

        if task is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task {task_id} not found"
            )

        return task


# ----------------------------
# Create Task
# ----------------------------
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    with Session(engine) as session:

        new_task = Task(
            title=task.title,
            done=False
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        return new_task


# ----------------------------
# Update Task
# ----------------------------
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):

    if updated_task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    with Session(engine) as session:

        task = session.get(Task, task_id)

        if task is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task {task_id} not found"
            )

        task.title = updated_task.title
        task.done = updated_task.done

        session.add(task)
        session.commit()
        session.refresh(task)

        return task


# ----------------------------
# Delete Task
# ----------------------------
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    with Session(engine) as session:

        task = session.get(Task, task_id)

        if task is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task {task_id} not found"
            )

        session.delete(task)
        session.commit()

        return