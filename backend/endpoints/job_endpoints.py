from fastapi import APIRouter, HTTPException
from config.db import get_database_connection
from schema.job import JobCreate, JobUpdate
from tasks.job_tasks import execute_job
from models.job import Job
from datetime import datetime, timezone
from models.job import ExecutionType
from helper import constants, job_helper, log
from sqlalchemy import distinct

router = APIRouter()
logger = log.setup_logging()


@router.get("/status")
async def get_distinct_job_statuses():
    """
    Get all distinct job statuses.

    Returns:
        list: List of distinct job statuses.
    """
    try:
        logger.info("Request received to fetch all distinct job statuses")
        with get_database_connection() as db:
            query = db.query(distinct(Job.status))
            statuses = [status[0] for status in query.all()]

            logger.info(
                "Distinct job statuses has been fetched successfully : %s", str(statuses))

            return statuses
    except Exception as e:
        db.rollback()

        logger.exception(
            "Failed to fetch all distinct job statuses: %s ", str(e))
        raise HTTPException(
            status_code=500, detail=constants.GENERIC_ERROR_MESSAGE)


@router.post("/")
async def create_job(job: JobCreate):
    """
    Create a new job.

    Args:
        job (JobCreate): The job data.

    Returns:
        dict: The created job.

    Raises:
        HTTPException: If the job could not be created.
    """
    try:
        with get_database_connection() as db:
            logger.info("Request received to create a job: %s", str(job))

            current_time = datetime.now(timezone.utc)
            execution_time = job.execution_time

            if execution_time <= current_time:
                logger.warning(
                    "Execution time should be greater than the current time: %s", execution_time)
                raise HTTPException(
                    status_code=500, detail="Please select the execution time which is greater than current time")

            # Check if a job with the same name already exists
            existing_job = db.query(Job).filter(Job.name == job.name).first()
            if existing_job:
                logger.warning(
                    "A job with the same name already exists: %s", job.name)
                raise HTTPException(
                    status_code=500, detail="A job with the same name already exists")

            db_job = Job(**job.dict())

            if db.query(ExecutionType).filter(ExecutionType.id == db_job.execution_type_id).first().to_json()['name'] == 'EVENT_BASED':
                if db_job.event_mapping_id is None:
                    logger.warning("Event mapping is missing for the job")
                    raise HTTPException(
                        status_code=500, detail="Event mapping is mandatory as you have select EVENT_BASED job.")

            db.add(db_job)
            db.commit()
            db.refresh(db_job)

            logger.info("Job created successfully: %s", str(db_job.to_json()))
            return db_job.to_json()

    except HTTPException as e:
        db.rollback()

        logger.exception(
            "Failed to create a job: %s", str(e))
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logger.exception(
            "Failed to create a job: %s", str(e))
        raise HTTPException(
            status_code=500, detail=constants.GENERIC_ERROR_MESSAGE)


@router.put("/{job_id}")
async def update_job(job_id: int, updated_job: JobUpdate):
    """
    Update a job.

    Args:
        job_id (int): The ID of the job to update.
        updated_job (JobUpdate): The updated job data.

    Returns:
        dict: The updated job.

    Raises:
        HTTPException: If the job could not be found.
    """
    try:
        with get_database_connection() as db:
            logger.info("Request received to update a job[%s]: %s", str(
                job_id), str(updated_job))
            job = db.query(Job).filter(Job.id == job_id).first()
            if not job:
                raise HTTPException(
                    status_code=404, detail=constants.JOB_NOT_FOUND)
            for attr, value in updated_job.dict(exclude_unset=True).items():
                setattr(job, attr, value)
            db.commit()
            db.refresh(job)

            logger.info("Job updated successfully: %s", str(job.to_json()))

            return job
    except HTTPException as e:
        db.rollback()

        logger.exception(
            "Failed to update a job: %s", str(e))
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.exception(
            "Failed to update a job: %s", str(e))
        raise HTTPException(
            status_code=500, detail=constants.GENERIC_ERROR_MESSAGE)


@router.get("/{job_id}")
async def get_job(job_id: int):
    """
    Get a job by ID.

    Args:
        job_id (int): The ID of the job to retrieve.

    Returns:
        dict: The job data.

    Raises:
        HTTPException: If the job could not be found.
    """
    try:
        logger.info(f"Fetching job {job_id}")
        with get_database_connection() as db:
            job = db.query(Job).filter(Job.id == job_id).first()
            if not job:
                raise HTTPException(
                    status_code=404, detail=constants.JOB_NOT_FOUND)

            logger.info(f"Job {job_id} fetched successfully")

            return job.to_json()

    except HTTPException as e:
        db.rollback()

        logger.error(f"Failed to fetch job {job_id}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.exception(
            f"An error occurred while fetching job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=constants.GENERIC_ERROR_MESSAGE)


@router.get("/")
async def get_jobs():
    """
    Get all jobs.

    Returns:
        list: List of jobs.
    """

    try:
        logger.info("Fetching all jobs")

        with get_database_connection() as db:
            jobs = db.query(Job).all()

            logger.info("Jobs fetched successfully")

            jobs = sorted(jobs, key=lambda job: (
                job.execution_time, job.priority))

            return [job.to_json() for job in jobs]

    except Exception as e:
        db.rollback()

        logger.exception(f"An error occurred while fetching jobs: {str(e)}")
        raise HTTPException(
            status_code=500, detail=constants.GENERIC_ERROR_MESSAGE)


@router.delete("/{job_id}")
async def delete_job(job_id: int):
    """
    Delete a job.

    Args:
        job_id (int): The ID of the job to delete.

    Returns:
        dict: A message indicating the job was deleted.

    Raises:
        HTTPException: If the job could not be found.
    """
    try:
        logger.info(f"Deleting job with ID: {job_id}")
        with get_database_connection() as db:
            job = db.query(Job).filter(Job.id == job_id).first()
            if not job:
                raise HTTPException(
                    status_code=404, detail=constants.JOB_NOT_FOUND)
            db.delete(job)
            db.commit()
            logger.info("Job deleted successfully")
            return {"message": "Job deleted"}
    except Exception as e:
        db.rollback()

        logger.exception(f"An error occurred while deleting the job: {str(e)}")
        raise HTTPException(
            status_code=500, detail=constants.GENERIC_ERROR_MESSAGE)


@router.post("/schedule-job/{job_id}")
async def schedule_job(job_id: int):
    """
    Schedule a job.

    Args:
        job_id (int): The ID of the job to schedule.

    Returns:
        dict: A message indicating the job has been scheduled.

    Raises:
        HTTPException: If the job could not be found or already stopped.
    """
    try:
        logger.info(f"Scheduling job with ID: {job_id}")

        with get_database_connection() as db:
            job = db.query(Job).filter(Job.id == job_id).first()
            if not job:
                raise HTTPException(
                    status_code=404, detail=constants.JOB_NOT_FOUND)

            if job.status == 'Failed':
                job.execution_time = datetime.now()

            job_helper.create_job_schedule(job, db)

            logger.info("Job scheduled successfully")

            return {"message": "Job has been scheduled successfully"}
    except Exception as e:
        db.rollback()

        logger.exception(
            f"An error occurred while scheduling the job: {str(e)}")
        raise HTTPException(
            status_code=500, detail=constants.GENERIC_ERROR_MESSAGE)

# Function to stop the job


@router.post("/stop-job/{job_id}")
async def stop_job(job_id: int):
    """
    Stop a job.

    Args:
        job_id (int): The ID of the job to stop.

    Returns:
        dict: A message indicating the job has been stopped.

    Raises:
        HTTPException: If the job could not be found or already stopped.
    """
    try:
        logger.info(f"Stopping job with ID: {job_id}")
        with get_database_connection() as db:
            job = db.query(Job).filter(Job.id == job_id).first()
            if not job:
                raise HTTPException(
                    status_code=404, detail=constants.JOB_NOT_FOUND)
            if job == 'Cancelled':
                raise HTTPException(
                    status_code=404, detail="Job has been already stopped")

            job_helper.stop_job_scheduler(job, db)
            logger.info("Job stopped successfully")

            return {"detail": "Job has been successfully stopped."}
    except Exception as e:
        db.rollback()

        logger.exception(f"An error occurred while stopping the job: {str(e)}")
        raise HTTPException(
            status_code=500, detail=constants.GENERIC_ERROR_MESSAGE)


@router.post("/event-notification/{event_id}")
async def handle_event_notification(event_id: str):

    with get_database_connection() as db:
        # Retrieve the job associated with the event_id
        job = db.query(Job).filter(Job.event_id == event_id).first()
        if not job:
            raise HTTPException(
                status_code=404, detail=constants.JOB_NOT_FOUND)

        # Execute the job
        execute_job.delay(job.id)

        return {"message": "Event notification received and job scheduled"}
