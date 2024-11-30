from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from typing import List
import uuid

from ..database.config import get_db
from ..models.token import DeviceToken
from ..schemas.token import TokenCreate, TokenResponse

router = APIRouter()

@router.post("/tokens", response_model=TokenResponse)
async def create_token(
    token: TokenCreate,
    db: AsyncSession = Depends(get_db)
):
    db_token = DeviceToken(
        user_id=token.user_id,
        token=token.token,
        platform=token.platform
    )
    
    try:
        db.add(db_token)
        await db.commit()
        await db.refresh(db_token)
        return db_token
    except IntegrityError:
        await db.rollback()
        # If token already exists, return the existing one
        query = select(DeviceToken).where(
            DeviceToken.user_id == token.user_id,
            DeviceToken.token == token.token,
            DeviceToken.platform == token.platform
        )
        result = await db.execute(query)
        existing_token = result.scalar_one_or_none()
        if existing_token:
            return existing_token
        raise HTTPException(status_code=400, detail="Token registration failed")

@router.get("/tokens/{user_id}", response_model=List[TokenResponse])
async def get_user_tokens(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    query = select(DeviceToken).where(DeviceToken.user_id == user_id)
    result = await db.execute(query)
    tokens = result.scalars().all()
    return tokens

@router.delete("/tokens/{token_id}")
async def delete_token(
    token_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    query = delete(DeviceToken).where(DeviceToken.id == token_id)
    result = await db.execute(query)
    await db.commit()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Token not found")
    
    return {"message": "Token deleted successfully"}