# PDF Report Generator

A FastAPI-based backend application that generates sales reports as PDF files using background jobs.

This project demonstrates how to move a slow report-generation operation out of the HTTP request, track its progress using a job ID, store the generated PDF, and provide a download endpoint.

---

## Assignment Information

| Field | Details |
|---|---|
| Assignment | PDF Report Generator |
| Assignment Code | BE-08 |
| Track | Backend AI Engineering |
| Week | Week 7 |
| Workload | 6 Hours |
| Phase | Build+ |

---

## Project Goal

Build a backend pipeline that:

1. Queries sales data from a database.
2. Performs SQL-based aggregation.
3. Generates a PDF report.
4. Runs PDF generation as a background job.
5. Returns a job ID immediately.
6. Tracks the job status.
7. Stores the generated PDF as an artifact.
8. Provides an endpoint to download the generated PDF.

---

## Features

- FastAPI REST API
- SQLite database
- SQLAlchemy ORM
- Sales data aggregation
- PDF report generation
- Background job processing
- Job status tracking
- Persistent job information
- PDF file storage
- PDF download endpoint
- Error handling for failed jobs
- Swagger/OpenAPI documentation

---

## Architecture

```text
                    Client
                      |
                      |
              POST /reports/generate
                      |
                      v
              Create Report Job
                      |
                      v
              SQLite: report_jobs
                      |
                      v
              Background Task
                      |
                      v
             Query Sales Data
                      |
                      v
             Aggregate Data
                      |
                      v
              Generate PDF
                      |
                      v
             Save PDF to /reports
                      |
                      v
              Update Job Status
                      |
                      v
              status = completed
                      |
             +--------+--------+
             |                 |
             v                 v
 GET /reports/{job_id}   GET /reports/{job_id}/download
             |                 |
             v                 v
       Job Status          PDF File
