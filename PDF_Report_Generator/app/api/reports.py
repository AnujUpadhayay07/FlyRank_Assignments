from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
import uuid
import os

from app.services.report_service import generate_pdf_report


router = APIRouter()

jobs = {}


def create_report_job(job_id):
    file_path = f"reports/{job_id}.pdf"

    jobs[job_id]["status"] = "processing"

    try:
        generate_pdf_report(file_path)

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["file"] = file_path

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)


@router.post("/reports/generate")
def generate_report(background_tasks: BackgroundTasks):

    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "job_id": job_id,
        "status": "queued"
    }

    background_tasks.add_task(create_report_job, job_id)

    return {
        "job_id": job_id,
        "status": "queued"
    }


@router.get("/reports/{job_id}")
def get_report_status(job_id: str):

    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return jobs[job_id]


@router.get(
    "/reports/{job_id}/download",
    responses={
        200: {
            "content": {
                "application/pdf": {}
            },
            "description": "PDF report file"
        },
        404: {
            "description": "Job or PDF file not found"
        },
        409: {
            "description": "Report is not ready"
        }
    }
)
def download_report(job_id: str):

    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    job = jobs[job_id]

    if job["status"] != "completed":
        raise HTTPException(
            status_code=409,
            detail=f"Report is not ready. Current status: {job['status']}"
        )

    file_path = job["file"]

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="PDF file not found"
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"report_{job_id}.pdf"
    )