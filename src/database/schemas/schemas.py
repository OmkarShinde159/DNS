from datetime import datetime
from pydantic import BaseModel,EmailStr
from enum import Enum
import uuid
from typing import Optional

class UserType(str, Enum):
    admin = "admin"
    owner = "owner"
    reporter = "reporter"


# session -------------------------------------------
class SessionBase(BaseModel):
    user_id : uuid.UUID
    created_at : Optional[datetime]
    logout_time: Optional[datetime]
    device_id : str
    device_ip : str
    access_token : str
    refresh_token: str
    is_active : bool
class UserBase(BaseModel):
    email: EmailStr
    password: str
   
class UserCreate(UserBase):
    user_type: UserType

    class Config:
        orm_mode = True

class UserOut(UserBase):
    id: Optional[uuid.UUID]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]

    class Config:
        orm_mode = True

class UserLogin(UserBase):
    user_id : str
    created_at : Optional[datetime]
    logout_time: Optional[datetime]
    device_id : Optional[str]
    device_ip : Optional[str]
    access_token : Optional[str]
    refresh_token: Optional[str]
    is_active : bool

    class Config:
        orm_mode = True


  

# token ---------------------------------------------------
class Token(BaseModel):
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: str
    # refresh_expires_in: int
    
class NewToken(BaseModel):
    access_token: str
    expires_in: int

    # refresh_expires_in: int
class TokenData(BaseModel):
    user_email: EmailStr | None = None
    user_password: str | None = None






   