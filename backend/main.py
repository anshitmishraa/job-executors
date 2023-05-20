from fastapi import FastAPI, Request
from config.db import get_database_connection
from endpoints.job_endpoints import router as job_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from endpoints.execution_type_endpoints import router as execution_type_router
from endpoints.event_mapping import router as event_mapping_router
from endpoints.job_type_endpoint import router as job_type_router
from helper import log
import os

logger = log.setup_logging()

templates = Jinja2Templates(directory="../frontend")

app = FastAPI()
current_directory = os.getcwd()
# Get the path of the parent directory
parent_directory = os.path.dirname(current_directory)
logger.info(current_directory)
logger.info(parent_directory)

app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")


@app.on_event("startup")
async def startup():
    with get_database_connection() as db:
        logger.info("Startup: Connected to the database")


@app.on_event("shutdown")
async def shutdown():
    """
    Event handler for the application shutdown event.

    Comments:
        This function is executed when the application receives a shutdown event.
        It is responsible for cleaning up any necessary resources before the application stops.

        Note: This function is specific to the framework being used (e.g., FastAPI, Starlette).
    """
    logger.info("Shutdown: Cleaning up resources")


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

app.include_router(job_router, prefix="/jobs", tags=["jobs"])
app.include_router(execution_type_router,
                   prefix="/execution_types", tags=["execution_types"])
app.include_router(event_mapping_router,
                   prefix="/event_mappings", tags=["event_mappings"])
app.include_router(job_type_router, prefix="/job_types", tags=["job_types"])
