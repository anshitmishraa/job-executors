from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class JobType(Base):
    """
    Model for the job type entity.

    Attributes:
        id (int): The ID of the job type.
        name (str): The name of the job type.
        description (str): The description of the job type.
        job_type (str): The type of the job.
        script (str): The script associated with the job type.
    """
    __tablename__ = 'job_type'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    job_type = Column(String)
    script = Column(String)

    def to_json(self):
        """
        Convert the JobType object to a JSON representation.

        Returns:
            dict: JSON representation of the JobType object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "job_type": self.job_type,
            "script": self.script
        }


class ExecutionType(Base):
    """
    Model for the execution type entity.

    Attributes:
        id (int): The ID of the execution type.
        name (str): The name of the execution type.
        description (str): The description of the execution type.
    """
    __tablename__ = 'execution_types'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    def to_json(self):
        """
        Convert the ExecutionType object to a JSON representation.

        Returns:
            dict: JSON representation of the ExecutionType object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class EventMapping(Base):
    """
    Model for the event mapping entity.

    Attributes:
        id (int): The ID of the event mapping.
        name (str): The name of the event mapping.
        description (str): The description of the event mapping.
    """
    __tablename__ = 'event_mappings'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    def to_json(self):
        """
        Convert the EventMapping object to a JSON representation.

        Returns:
            dict: JSON representation of the EventMapping object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class Job(Base):
    """
    Model for the job entity.

    Attributes:
        id (int): The ID of the job.
        name (str): The name of the job.
        execution_type_id (int): The ID of the execution type associated with the job.
        execution_time (datetime): The execution time of the job.
        recurring (bool): Indicates whether the job is recurring.
        event_mapping_id (int): The ID of the event mapping associated with the job.
        priority (int): The priority of the job.
        created_at (datetime): The timestamp when the job was created.
        updated_at (datetime): The timestamp when the job was last updated.
        status (str): The status of the job.
        job_type_id (int): The ID of the job type associated with the job.
        job_scheduler_id (str): The ID of the job scheduler associated with the job.
    """
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    execution_type_id = Column(Integer, ForeignKey('execution_types.id'))
    execution_time = Column(DateTime)
    recurring = Column(Boolean, default=False)
    event_mapping_id = Column(Integer, ForeignKey('event_mappings.id'))
    priority = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    status = Column(String, default="Scheduled")
    job_type_id = Column(Integer, ForeignKey('job_type.id'))
    job_scheduler_id = Column(String)

    execution_type = relationship("ExecutionType")
    event_mapping = relationship("EventMapping")
    job_type = relationship("JobType")

    def to_json(self):
        """
        Convert the Job object to a JSON representation.

        Returns:
            dict: JSON representation of the Job object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "execution_type_id": self.execution_type_id,
            "execution_time": self.execution_time,
            "recurring": self.recurring,
            "event_mapping_id": self.event_mapping_id,
            "priority": self.priority,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "job_type_id": self.job_type_id,
            "job_scheduler_id": self.job_scheduler_id
        }
