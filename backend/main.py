from fastapi import FastAPI
import os

from backend.endpoints.job_endpoints import router as job_router
from backend.config.db import get_database_connection
from backend.endpoints.execution_type_endpoints import router as execution_type_router
from backend.endpoints.event_mapping import router as event_mapping_router
from backend.endpoints.job_type_endpoint import router as job_type_router
from backend.helper import log

logger = log.setup_logging()


app = FastAPI()
current_directory = os.getcwd()
# Get the path of the parent directory
parent_directory = os.path.dirname(current_directory)
logger.info(current_directory)
logger.info(parent_directory)


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


app.include_router(job_router, prefix="/jobs", tags=["jobs"])
app.include_router(execution_type_router,
                   prefix="/execution_types", tags=["execution_types"])
app.include_router(event_mapping_router,
                   prefix="/event_mappings", tags=["event_mappings"])
app.include_router(job_type_router, prefix="/job_types", tags=["job_types"])
