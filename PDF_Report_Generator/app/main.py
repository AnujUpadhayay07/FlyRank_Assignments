from fastapi import FastAPI

from app.db.database import engine, Base
from app.models.submission import Sale
from app.services.report_service import get_report_data
from app.api.reports import router as reports_router
from app.models.report_job import ReportJob

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PDF Report Generator")


@app.get("/")
def home():
    return {
        "message": "PDF Report Generator API is running"
    }


@app.get("/report-data")
def report_data():
    return get_report_data()


app.include_router(reports_router)