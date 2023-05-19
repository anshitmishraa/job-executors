from fastapi import APIRouter, HTTPException
from config.db import get_database_connection
from schema.job_type import JobTypeCreate, JobTypeUpdate
from models.job import JobType

router = APIRouter()


@router.post("/")
async def create_job_type(job_type: JobTypeCreate):
    """
    Create a new job type.

    Args:
        job_type (JobTypeCreate): The job type data.

    Returns:
        dict: The created job type.

    Raises:
        HTTPException: If the job type is missing the script attribute when the job type is 'SCRIPT'.
    """
    if job_type.job_type == 'SCRIPT' and job_type.script == None:
        raise HTTPException(
            status_code=400, detail="Script can't be blank here")

    with get_database_connection() as db:
        db_job_type = JobType(**job_type.dict())
        db.add(db_job_type)
        db.commit()
        db.refresh(db_job_type)
        return db_job_type.to_json()


@router.get("/")
async def get_job_types():
    """
    Get all job types.

    Returns:
        list: List of job types.
    """
    with get_database_connection() as db:
        job_types = db.query(JobType).all()
        return [job_type.to_json() for job_type in job_types]


@router.put("/{job_type_id}")
async def update_job_type(job_type_id: int, updated_job_type: JobTypeUpdate):
    """
    Update a job type.

    Args:
        job_type_id (int): The ID of the job type to update.
        updated_job_type (JobTypeUpdate): The updated job type data.

    Returns:
        dict: The updated job type.

    Raises:
        HTTPException: If the job type could not be found.
    """
    with get_database_connection() as db:
        job_type = db.query(JobType).filter(
            JobType.id == job_type_id).first()
        if not job_type:
            raise HTTPException(
                status_code=404, detail="Job Type not found")
        for attr, value in updated_job_type.dict(exclude_unset=True).items():
            setattr(job_type, attr, value)
        db.commit()
        db.refresh(job_type)
        return job_type


@router.get("/{job_type_id}")
async def get_job_type(job_type_id: int):
    """
    Get a job type by ID.

    Args:
        job_type_id (int): The ID of the job type to retrieve.

    Returns:
        dict: The job type data.

    Raises:
        HTTPException: If the job type could not be found.
    """
    with get_database_connection() as db:
        job_type = db.query(JobType).filter(
            JobType.id == job_type_id).first()
        if not job_type:
            raise HTTPException(
                status_code=404, detail="Job Type not found")
        return job_type.to_json()


@router.delete("/{job_type_id}")
async def delete_job_type(job_type_id: int):
    """
    Delete a job type.

    Args:
        job_type_id (int): The ID of the job type to delete.

    Returns:
        dict: A message indicating the job type was deleted.

    Raises:
        HTTPException: If the job type could not be found.
    """
    with get_database_connection() as db:
        job_type = db.query(JobType).filter(
            JobType.id == job_type_id).first()
        if not job_type:
            raise HTTPException(
                status_code=404, detail="Job Type not found")
        db.delete(job_type)
        db.commit()
        return {"message": "Job Type deleted"}
