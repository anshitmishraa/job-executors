from fastapi import FastAPI

from backend.config.db import get_database_connection
from backend.helper import log

logger = log.setup_logging()


app = FastAPI()


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
