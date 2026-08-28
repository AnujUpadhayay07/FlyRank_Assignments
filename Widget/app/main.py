from fastapi import FastAPI

from app.api.routes.user import router as user_router
from app.api.routes.tenant import router as tenant_router
from app.api.routes.widget import router as widget_router
from app.api.routes.submission import router as submission_router


app = FastAPI(
    title="Embeddable Widget & Lead-Capture Platform",
    version="1.0.0",
)


app.include_router(tenant_router)
app.include_router(user_router)
app.include_router(widget_router)
app.include_router(submission_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "widget-platform",
    }