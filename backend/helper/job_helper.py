from apscheduler.triggers.date import DateTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time, timedelta
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.base import BaseTrigger

from backend.models.job import ExecutionType, EventMapping
from backend.models.job import Job
from backend.tasks import job_tasks
from backend.helper import log

scheduler = BackgroundScheduler()
scheduler.start()
logger = log.setup_logging()


def create_job_schedule(job: Job, db):
    """
    Create a schedule for a job based on its execution type.

    Args:
        job (Job): The job to schedule.
        db: The database connection.

    Raises:
        Exception: If an invalid execution type is provided.
    """
    execution_type = (
        db.query(ExecutionType)
        .filter(ExecutionType.id == job.execution_type_id)
        .first()
    )

    event_mapping = (
        db.query(EventMapping).filter(ExecutionType.id == job.event_mapping_id).first()
    )

    if execution_type.name == "TIME_SPECIFIC":
        if job.recurring:
            # Specify the time at which the job should run every day
            execution_time = time(
                hour=job.execution_time.hour,
                minute=job.execution_time.minute,
                second=job.execution_time.second,
            )

            # Get the current date
            current_date = datetime.now().date()

            # Combine the current date and execution time to create a datetime object
            execution_datetime = datetime.combine(current_date, execution_time)

            # Create an IntervalTrigger with a daily interval
            trigger = IntervalTrigger(days=1, start_date=execution_datetime)

            # Add the job with the recurring trigger
            job_scheduler_response = scheduler.add_job(
                job_tasks.execute_job,
                args=[job.id],
                trigger=trigger,
                priority=job.priority,
            )

            logger.info("Job has been scheduled: " + str(job_scheduler_response))
            job.job_scheduler_id = job_scheduler_response.id
        else:
            trigger = DateTrigger(run_date=job.execution_time)
            job_scheduler_response = scheduler.add_job(
                job_tasks.execute_job,
                args=[job.id],
                trigger=trigger,
                priority=job.priority,
            )
            logger.info("Job has been scheduled: " + str(job_scheduler_response))
            job.job_scheduler_id = job_scheduler_response.id

    elif execution_type.name == "EVENT_BASED":
        # Replace 60*60 with the desired delay in seconds
        future_datetime = datetime.now() + timedelta(weeks=100)

        trigger = DateTrigger(run_date=future_datetime)

        job_scheduler_response = scheduler.add_job(
            job_tasks.execute_job, trigger=trigger, args=[job.id], priority=job.priority
        )

        logger.info("Job has been scheduled: " + str(job_scheduler_response))

        job.job_scheduler_id = job_scheduler_response.id

        job.execution_time = future_datetime

    db.commit()


def stop_job_scheduler(job: Job, db):
    """
    Stop a scheduled job.

    Args:
        job (Job): The job to stop.
        db: The database connection.
    """
    try:
        logger.info(f"Stopping job scheduler for job ID: {job.id}")

        scheduler.remove_job(job.job_scheduler_id)

        job.status = "Cancelled"
        job.updated_at = datetime.now()
        db.commit()

        logger.info("Job scheduler stopped successfully")
    except Exception as e:
        logger.exception(f"An error occurred while stopping job scheduler: {str(e)}")


def update_job_schedule(job: Job, db):
    """
    Update a scheduled for a job based on its execution type.

    Args:
        job (Job): The job to schedule.
        db: The database connection.

    Raises:
        Exception: If an invalid execution type is provided.
    """
    execution_type = (
        db.query(ExecutionType)
        .filter(ExecutionType.id == job.execution_type_id)
        .first()
    )

    event_mapping = (
        db.query(EventMapping).filter(ExecutionType.id == job.event_mapping_id).first()
    )

    if execution_type.name == "TIME_SPECIFIC":
        if job.recurring:
            # Specify the time at which the job should run every day
            execution_time = time(
                hour=job.execution_time.hour,
                minute=job.execution_time.minute,
                second=job.execution_time.second,
            )

            # Get the current date
            current_date = datetime.now().date()

            # Combine the current date and execution time to create a datetime object
            execution_datetime = datetime.combine(current_date, execution_time)

            # Create an IntervalTrigger with a daily interval
            trigger = IntervalTrigger(days=1, start_date=execution_datetime)

            # Add the job with the recurring trigger
            job_scheduler_response = scheduler.modify_job(
                job.job_scheduler_id, trigger=trigger
            )

            logger.info("Job has been scheduled: " + str(job_scheduler_response))
            job.job_scheduler_id = job_scheduler_response.id
        else:
            trigger = DateTrigger(run_date=job.execution_time)
            job_scheduler_response = scheduler.modify_job(
                job.job_scheduler_id, trigger=trigger
            )
            logger.info("Job has been scheduled: " + str(job_scheduler_response))
            job.job_scheduler_id = job_scheduler_response.id

    elif execution_type.name == "EVENT_BASED":
        future_datetime = time.time() + 60 * 60

        job_scheduler_response = scheduler.modify_job(
            job.job_scheduler_id, "date", run_date=future_datetime, args=[job.id]
        )

        logger.info("Job has been scheduled: " + str(job_scheduler_response))

        job.job_scheduler_id = job_scheduler_response.id

    db.commit()
