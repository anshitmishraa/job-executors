from helper import job_helper, log
from config.db import get_database_connection
from models.job import Job
from datetime import datetime
from dotenv import load_dotenv
from models.job import JobType
from script import run_script as script

load_dotenv()

logger = log.setup_logging()


def execute_job(job_id):
    with get_database_connection() as db:
        """
        Execute a job based on its configuration.

        Args:
        job_id (int): The ID of the job to execute.
        """
        try:

            job = db.query(Job).filter(Job.id == job_id).first()
            if not job:
                raise Exception("Job not found")

            result_job = job.to_json()

            job_type = db.query(JobType).filter(
                JobType.id == result_job['job_type_id']).first()
            if not job_type:
                raise Exception("Job Type not found")

            result_job_type = job_type.to_json()

            logger.info("Executing job: %s", result_job['name'])
            logger.info("Job details: %s", str(result_job))
            logger.info("Job type details: %s", str(result_job_type))

            if result_job['recurring']:
                result_job['excecution_time'] = result_job['excecution_time'] + \
                    datetime.timedelta(days=1)

                job_helper.create_job_schedule(result_job, db)

            # Execute the job based on its execution_type and other configuration
            if result_job_type['job_type'] == "CODE":
                if result_job_type['name'] == "COUNT_TILL_10":
                    logger.info("Executing COUNT_TILL_10 job")

                    countTillTen = 0

                    while countTillTen < 10:

                        countTillTen = countTillTen + 1

                        job.status = "Running"

                    # Update the job status based on the API response
                    if countTillTen == 10:
                        job.status = "Completed"
                    else:
                        job.status = "Failed"
            elif result_job_type['job_type'] == "SCRIPT":
                logger.info("Executing SCRIPT job")

                if script.run_script(result_job_type):
                    job.status = "Completed"
                else:
                    logger.error("SCRIPT job failed")

                    job.status = "Failed"
                # Handle event-based execution
            elif result_job_type['name'] == "EVENT_BASED":
                # Listen for the specific event
                # Example code: (Please note this is a placeholder and you need to replace it with your actual event handling logic)
                event_occurred = listen_for_event(result_job['event_name'])
                if event_occurred:
                    # Perform the job-specific logic here when the event occurs
                    # ...

                    # You can also update the job status during the execution if needed
                    job.status = "Running"
                    db.commit()
                else:
                    # Handle the case when the event doesn't occur or handle the event not found scenario
                    job.status = "Failed"
                    db.commit()
            else:
                # Unknown execution_type
                job.status = "Failed"

            # Update job status and other relevant information
            job.updated_at = datetime.now()
            db.commit()
            logger.info("Job execution completed successfully.")

        except Exception as e:
            db.rollback()
            job.status = "Failed"
            logger.exception(
                "An error occurred during job execution: %s", str(e))
            raise
