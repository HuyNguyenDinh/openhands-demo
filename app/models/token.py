from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, Index
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from ..database.config import Base

class PlatformEnum(str, enum.Enum):
    FCM = "fcm"
    APNS = "apns"

class DeviceToken(Base):
    __tablename__ = "device_tokens"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)
    token = Column(String, nullable=False)
    platform = Column(SQLEnum(PlatformEnum), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('idx_user_token_platform', user_id, token, platform, unique=True),
    )