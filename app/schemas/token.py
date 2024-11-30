from pydantic import BaseModel, UUID4
from datetime import datetime
from ..models.token import PlatformEnum
from typing import Optional

class TokenBase(BaseModel):
    user_id: str
    token: str
    platform: PlatformEnum

class TokenCreate(TokenBase):
    pass

class TokenResponse(TokenBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True