from datetime import datetime as dt
import uuid

from sqlalchemy import (
    Column,
    DateTime,
    String,
)
from sqlalchemy.dialects.postgresql import ENUM, UUID
from src.database.database import Base
from src.database.schemas.schemas import UserType

class User(Base):
    '''
    model class for user table
    '''
    __tablename__= "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_type = Column(ENUM(UserType, name="user_type",create_type=False),nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=dt.now)
    modified_at= Column(DateTime, default=dt.now)
    

