from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_async_session
from models.models import operation
from operations.schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operations"]
)

@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.all(),
            "detalis": None
        }
    except:
        raise HTTPException(status_code = 500, detail={
            "status": "error",
            "data": None,
            "details": None
        })

@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):

    try:
        stmt = insert(operation).values(**new_operation.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
        }
    except Exception:
        raise HTTPException(status_code=501, detail={
         "status": "error",
     })
