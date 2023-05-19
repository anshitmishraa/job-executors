from pydantic import BaseModel


class EventMappingBase(BaseModel):
    """
    Base model for event mapping.

    Attributes:
        name (str): The name of the event mapping.
        description (str): The description of the event mapping.
    """
    name: str
    description: str


class EventMappingCreate(EventMappingBase):
    """
    Model for creating an event mapping.

    Inherits:
        EventMappingBase: Base model for event mapping.
    """
    pass


class EventMappingUpdate(EventMappingBase):
    """
    Model for updating an event mapping.

    Inherits:
        EventMappingBase: Base model for event mapping.
    """
    pass


class EventMappingResponse(EventMappingBase):
    """
    Model for the response of an event mapping.

    Inherits:
        EventMappingBase: Base model for event mapping.

    Attributes:
        id (int): The ID of the event mapping.
    """
    id: int


class EventMappingDB(EventMappingBase):
    """
    Model for the event mapping stored in the database.

    Inherits:
        EventMappingBase: Base model for event mapping.

    Attributes:
        id (int): The ID of the event mapping.

    Config:
        orm_mode (bool): Enables ORM mode for the model, allowing it to work with the database.
    """
    id: int

    class Config:
        orm_mode = True
