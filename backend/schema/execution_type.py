from pydantic import BaseModel


class ExecutionTypeBase(BaseModel):
    """
    Base model for execution types.

    Attributes:
        name (str): The name of the execution type.
        description (str): The description of the execution type.
    """
    name: str
    description: str


class ExecutionTypeCreate(ExecutionTypeBase):
    """
    Model for creating an execution type.

    Inherits:
        ExecutionTypeBase: Base model for execution types.
    """
    pass


class ExecutionTypeUpdate(ExecutionTypeBase):
    """
    Model for updating an execution type.

    Inherits:
        ExecutionTypeBase: Base model for execution types.
    """
    pass


class ExecutionTypeResponse(ExecutionTypeBase):
    """
    Model for the response of an execution type.

    Inherits:
        ExecutionTypeBase: Base model for execution types.

    Attributes:
        id (int): The ID of the execution type.
    """
    id: int


class ExecutionTypeDB(ExecutionTypeBase):
    """
    Model for the execution type stored in the database.

    Inherits:
        ExecutionTypeBase: Base model for execution types.

    Attributes:
        id (int): The ID of the execution type.

    Config:
        orm_mode (bool): Enables ORM mode for the model, allowing it to work with the database.
    """
    id: int

    class Config:
        orm_mode = True
