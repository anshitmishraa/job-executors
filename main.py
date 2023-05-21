from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from backend.endpoints.job_endpoints import router as job_router
from backend.endpoints.execution_type_endpoints import router as execution_type_router
from backend.endpoints.event_mapping import router as event_mapping_router
from backend.endpoints.job_type_endpoint import router as job_type_router

app = FastAPI()

# Mount the static files directory
app.mount("/frontend", StaticFiles(directory="./frontend"), name="frontend")
templates = Jinja2Templates(directory="./frontend")


@app.get("/")
async def home(request: Request):
    """
    Handler for the home route.

    Args:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The rendered HTML template response.

    Comments:
        This handler serves as the entry point for the home route ("/").
        It renders the "index.html" template and passes the request context to it.
    """
    context = {"request": request}
    return templates.TemplateResponse("index.html", context=context)


@app.get("/health")
def check_health():
    return {"status": "OK"}


# Include the API routes from api/main.py
app.include_router(job_router, prefix="/jobs", tags=["jobs"])
app.include_router(
    execution_type_router, prefix="/execution_types", tags=["execution_types"]
)
app.include_router(
    event_mapping_router, prefix="/event_mappings", tags=["event_mappings"]
)
app.include_router(job_type_router, prefix="/job_types", tags=["job_types"])
