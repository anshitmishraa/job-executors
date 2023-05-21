from fastapi import HTTPException
from datetime import datetime, timezone

from backend.models.job import Job


# Check if a job with the same name already exists


def validate_job_name(db, name):
    existing_job = db.query(Job).filter(Job.name == name).first()
    if existing_job:
        raise HTTPException(
            status_code=500, detail="A job with the same name already exists"
        )


# Check if a job execution time is less than the current time
def validate_execution_time(execution_time):
    current_time = datetime.now(timezone.utc)
    if execution_time <= current_time:
        raise HTTPException(
            status_code=500,
            detail="Please select an execution time greater than the current time",
        )


def validate_event_mapping(db, event_mapping_id):
    existing_job_mapping = (
        db.query(Job).filter(Job.event_mapping_id == event_mapping_id).first()
    )
    if existing_job_mapping:
        raise HTTPException(
            status_code=500, detail="A job with the same event already exists"
        )


def validate_event_mapping_required(execution_type, event_mapping_id):
    if execution_type == "EVENT_BASED" and event_mapping_id is None:
        raise HTTPException(
            status_code=500, detail="Event mapping is mandatory for EVENT_BASED jobs"
        )


def validate_existing_job_name(db, job):
    existing_job = db.query(Job).filter(Job.name == job.name).first()
    if existing_job.id != job.id:
        raise HTTPException(
            status_code=500, detail="A job with the same name already exists"
        )
