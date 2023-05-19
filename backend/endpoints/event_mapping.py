from fastapi import APIRouter, HTTPException
from config.db import get_database_connection
from schema.event_mapping import EventMappingCreate, EventMappingUpdate
from models.job import EventMapping

router = APIRouter()


@router.post("/")
async def create_event_mapping(event_mapping: EventMappingCreate):
    """
    Create a new event mapping.

    Args:
        event_mapping (EventMappingCreate): The event mapping data.

    Returns:
        dict: The created event mapping.

    Raises:
        HTTPException: If the event mapping could not be created.
    """
    with get_database_connection() as db:
        db_event_mapping = EventMapping(**event_mapping.dict())
        db.add(db_event_mapping)
        db.commit()
        db.refresh(db_event_mapping)
        return db_event_mapping


@router.get("/")
async def get_event_mappings():
    """
    Get all event mappings.

    Returns:
        list: List of event mappings in JSON format.
    """
    with get_database_connection() as db:
        event_mappings = db.query(EventMapping).all()
        return [event_mapping.to_json() for event_mapping in event_mappings]


@router.put("/{event_mapping_id}")
async def update_event_mapping(event_mapping_id: int, updated_event_mapping: EventMappingUpdate):
    """
    Update an event mapping.

    Args:
        event_mapping_id (int): The ID of the event mapping to update.
        updated_event_mapping (EventMappingUpdate): The updated event mapping data.

    Returns:
        dict: The updated event mapping.

    Raises:
        HTTPException: If the event mapping could not be found.
    """
    with get_database_connection() as db:
        event_mapping = db.query(EventMapping).filter(
            EventMapping.id == event_mapping_id).first()
        if not event_mapping:
            raise HTTPException(
                status_code=404, detail="Event Mapping not found")
        for attr, value in updated_event_mapping.dict(exclude_unset=True).items():
            setattr(event_mapping, attr, value)
        db.commit()
        db.refresh(event_mapping)
        return event_mapping


@router.get("/{event_mapping_id}")
async def get_event_mapping(event_mapping_id: int):
    """
    Get an event mapping by ID.

    Args:
        event_mapping_id (int): The ID of the event mapping to retrieve.

    Returns:
        dict: The event mapping in JSON format.

    Raises:
        HTTPException: If the event mapping could not be found.
    """
    with get_database_connection() as db:
        event_mapping = db.query(EventMapping).filter(
            EventMapping.id == event_mapping_id).first()
        if not event_mapping:
            raise HTTPException(
                status_code=404, detail="Event Mapping not found")
        return event_mapping.to_json()


@router.delete("/{event_mapping_id}")
async def delete_event_mapping(event_mapping_id: int):
    """
    Delete an event mapping.

    Args:
        event_mapping_id (int): The ID of the event mapping to delete.

    Returns:
        dict: A message indicating the event mapping was deleted.

    Raises:
        HTTPException: If the event mapping could not be found.
    """
    with get_database_connection() as db:
        event_mapping = db.query(EventMapping).filter(
            EventMapping.id == event_mapping_id).first()
        if not event_mapping:
            raise HTTPException(
                status_code=404, detail="Event Mapping not found")
        db.delete(event_mapping)
        db.commit()
        return {"message": "Event Mapping deleted"}
