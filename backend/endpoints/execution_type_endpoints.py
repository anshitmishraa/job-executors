from fastapi import APIRouter, HTTPException

from backend.config.db import get_database_connection
from backend.schema.execution_type import ExecutionTypeCreate, ExecutionTypeUpdate
from backend.models.job import ExecutionType

router = APIRouter()


@router.get("/")
async def get_execution_types():
    """
    Get all execution types.

    Returns:
        list: List of execution types in JSON format.
    """
    with get_database_connection() as db:
        execution_types = db.query(ExecutionType).all()
        return [execution_type.to_json() for execution_type in execution_types]


@router.post("/")
async def create_execution_type(execution_type: ExecutionTypeCreate):
    """
    Create a new execution type.

    Args:
        execution_type (ExecutionTypeCreate): The execution type data.

    Returns:
        dict: The created execution type.

    Raises:
        HTTPException: If the execution type could not be created.
    """
    with get_database_connection() as db:
        db_execution_type = ExecutionType(**execution_type.dict())
        db.add(db_execution_type)
        db.commit()
        db.refresh(db_execution_type)
        return db_execution_type


@router.put("/{execution_type_id}")
async def update_execution_type(execution_type_id: int, updated_execution_type: ExecutionTypeUpdate):
    """
    Update an execution type.

    Args:
        execution_type_id (int): The ID of the execution type to update.
        updated_execution_type (ExecutionTypeUpdate): The updated execution type data.

    Returns:
        dict: The updated execution type.

    Raises:
        HTTPException: If the execution type could not be found.
    """
    with get_database_connection() as db:
        execution_type = db.query(ExecutionType).filter(
            ExecutionType.id == execution_type_id).first()
        if not execution_type:
            raise HTTPException(
                status_code=404, detail="Execution Type not found")
        for attr, value in updated_execution_type.dict(exclude_unset=True).items():
            setattr(execution_type, attr, value)
        db.commit()
        db.refresh(execution_type)
        return execution_type


@router.get("/{execution_type_id}")
async def get_execution_type(execution_type_id: int):
    """
    Get an execution type by ID.

    Args:
        execution_type_id (int): The ID of the execution type to retrieve.

    Returns:
        dict: The execution type in JSON format.

    Raises:
        HTTPException: If the execution type could not be found.
    """
    with get_database_connection() as db:
        execution_type = db.query(ExecutionType).filter(
            ExecutionType.id == execution_type_id).first()
        if not execution_type:
            raise HTTPException(
                status_code=404, detail="Execution Type not found")
        return execution_type.to_json()


@router.delete("/{execution_type_id}")
async def delete_execution_type(execution_type_id: int):
    """
    Delete an execution type.

    Args:
        execution_type_id (int): The ID of the execution type to delete.

    Returns:
        dict: A message indicating the execution type was deleted.

    Raises:
        HTTPException: If the execution type could not be found.
    """
    with get_database_connection() as db:
        execution_type = db.query(ExecutionType).filter(
            ExecutionType.id == execution_type_id).first()
        if not execution_type:
            raise HTTPException(
                status_code=404, detail="Execution Type not found")
        db.delete(execution_type)
        db.commit()
        return {"detail": "Execution Type deleted"}
