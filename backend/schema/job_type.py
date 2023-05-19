from pydantic import BaseModel


class JobTypeBase(BaseModel):
    """
    Base model for job types.

    Attributes:
        name (str): The name of the job type.
        job_type (str): The type of the job.
    """
    name: str
    job_type: str


class JobTypeCreate(JobTypeBase):
    """
    Model for creating a job type.

    Inherits:
        JobTypeBase: Base model for job types.
    """
    script: str
    pass


class JobTypeUpdate(JobTypeBase):
    """
    Model for updating a job type.

    Inherits:
        JobTypeBase: Base model for job types.
    """
    pass


class JobTypeResponse(JobTypeBase):
    """
    Model for the response of a job type.

    Inherits:
        JobTypeBase: Base model for job types.

    Attributes:
        id (int): The ID of the job type.
        script (str): The script associated with the job type.
        description (str): The description of the job type.
    """
    id: int
    script: str
    description: str


class JobTypeDB(JobTypeBase):
    """
    Model for the job type stored in the database.

    Inherits:
        JobTypeBase: Base model for job types.

    Attributes:
        id (int): The ID of the job type.
        script (str): The script associated with the job type.
        description (str): The description of the job type.

    Config:
        orm_mode (bool): Enables ORM mode for the model, allowing it to work with the database.
    """
    id: int
    script: str
    description: str

    class Config:
        orm_mode = True
