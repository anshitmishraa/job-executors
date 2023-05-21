from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class JobBase(BaseModel):
    """
    Base model for jobs.

    Attributes:
        name (str): The name of the job.
        execution_type_id (int): The ID of the execution type associated with the job.
        job_type_id (int): The ID of the job type associated with the job.
        execution_time (datetime): The execution time of the job.
        recurring (bool): Indicates whether the job is recurring.
        priority (int): The priority of the job.
    """
    name: str
    execution_type_id: int
    job_type_id: int
    execution_time: datetime
    recurring: bool
    priority: int


class JobCreate(JobBase):
    """
    Model for creating a job.

    Inherits:
        JobBase: Base model for jobs.
        event_mapping_id (int): The ID of the event mapping associated with the job.
    """
    event_mapping_id: int
    pass


class JobUpdate(JobBase):
    """
    Model for updating a job.

    Inherits:
        JobBase: Base model for jobs.

    Attributes:
        job_scheduler_id (str): The ID of the job scheduler associated with the job.
        status (str): The status of the job.
    """
    job_scheduler_id: str
    status: str
    pass


class JobResponse(JobBase):
    """
    Model for the response of a job.

    Inherits:
        JobBase: Base model for jobs.

    Attributes:
        id (int): The ID of the job.
        status (str): The status of the job.
        event_mapping_id (int): The ID of the event mapping associated with the job.
        created_at (datetime): The timestamp when the job was created.
        updated_at (datetime): The timestamp when the job was last updated.
        job_scheduler_id (str): The ID of the job scheduler associated with the job.
    """
    id: int
    status: str
    event_mapping_id: int
    created_at: datetime
    updated_at: datetime
    job_scheduler_id: str


class JobDB(JobBase):
    """
    Model for the job stored in the database.

    Inherits:
        JobBase: Base model for jobs.

    Attributes:
        id (int): The ID of the job.
        status (str): The status of the job.
        event_mapping_id (int): The ID of the event mapping associated with the job.
        created_at (datetime): The timestamp when the job was created.
        updated_at (datetime): The timestamp when the job was last updated.
        job_scheduler_id (str): The ID of the job scheduler associated with the job.

    Config:
        orm_mode (bool): Enables ORM mode for the model, allowing it to work with the database.
    """
    id: int
    status: str
    event_mapping_id: int
    created_at: datetime
    updated_at: datetime
    job_scheduler_id: str

    class Config:
        orm_mode = True
