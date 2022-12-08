from datetime import datetime as dt
import uuid
from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column,
    DateTime,
    String,
    ForeignKey,
    Boolean
)
from sqlalchemy.dialects.postgresql import ENUM, UUID
from src.database.database import Base
from src.database.schemas.schemas import UserType

class User(Base):
    __tablename__= "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,unique=True)
    user_type = Column(ENUM(UserType, name="user_type",create_type=False),nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=dt.now)
    modified_at= Column(DateTime)
    # sessions_rel = relationship("Session")
    

class Session(Base):
    __tablename__= "sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    created_at = Column(DateTime,nullable=False)
    logout_time= Column(DateTime)
    device_id = Column(String(255), nullable=False)
    device_ip = Column(String(255), nullable=False)
    access_token = Column(String, nullable=False)
    refresh_token= Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    users_rel = relationship("User")



