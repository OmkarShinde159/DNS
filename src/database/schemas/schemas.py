from datetime import datetime
from pydantic import BaseModel,EmailStr
from enum import Enum
import uuid
from typing import Optional

class UserType(str, Enum):
    admin = "admin"
    owner = "owner"
    reporter = "reporter"

class UserBase(BaseModel):
    user_type: UserType
    email: EmailStr
    password: str
   
class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    user_id: Optional[uuid.UUID]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]

    class Config:
        orm_mode = True

