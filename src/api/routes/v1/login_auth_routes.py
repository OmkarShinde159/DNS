
from src.database.schemas import schemas
from src.database import models
from fastapi import status,HTTPException,Depends,APIRouter
from src.database.database import get_db
from sqlalchemy.orm import Session
from src.api.routes.v1 import signup_route
from src.utils import utils
from src.core.config import settings
from src.database.models import User
from fastapi import Header
from src.api.routes.v1 import session_routes as s

from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY= settings.secret_key
REFRESH_SECRET_KEY= settings.refresh_secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES= settings.refresh_token_expire_minutes
# REFRESH_TOKEN_EXPIRE_MINUTES= 60
# REFRESH_SECRET_KEY= "b139f73aafc0ebbb5565ee59753ecf0b40c04bbf1facf4f85db26f1643da46f1"

# print(ACCESS_TOKEN_EXPIRE_MINUTES)
# print(REFRESH_TOKEN_EXPIRE_MINUTES)
# print(type(REFRESH_TOKEN_EXPIRE_MINUTES))
# print(REFRESH_SECRET_KEY)
# print(type(REFRESH_SECRET_KEY))


def create_access_token(data: dict):
    to_encode = data.copy()
    # check value & type
    # print(ACCESS_TOKEN_EXPIRE_MINUTES)
    # print(type(ACCESS_TOKEN_EXPIRE_MINUTES))

    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode_ref = data.copy()
    # check value & type
    # print(REFRESH_TOKEN_EXPIRE_MINUTES)
    # print(type(REFRESH_TOKEN_EXPIRE_MINUTES))

    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode_ref.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode_ref, REFRESH_SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email:str = payload.get("user_email")
        # password:str = payload.get("user_password")
        if email is None:
        # if (email and password) is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_email=email)
        # token_data = schemas.TokenData(user_email=email, user_password=password)
    except JWTError:
        raise credentials_exception

    return token_data
    # TODO :replace email and pw with user_id and user_type in token data



def get_current_user(token: str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            message=f'could not validate credentials', 
                            headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.email == token.user_email)

    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# authenticate user ----------------------------------------------------------------------
router = APIRouter( 
    prefix="/login",
    tags = ['Authentication']
)


'''

@router.post("/",response_model=schemas.Token)
def login(user_credential:schemas.UserLogin, db: Session = Depends(get_db)):
    user = signup_route.verify_email(db,user_credential.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credential")

    elif not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid Credentials")
    
    else:
    # create token
    # token_data = schemas.UserLogin
        # token_data = {"user_email":user.email,
        # "user_password":user.password}
        token_data = {"user_email":user.email}
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        

        return {"access_token":access_token,
                "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES,
                "token_type":"bearer",
                "refresh_token": refresh_token}

'''   
        
 
'''
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_email=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data, username=token_data.user_email)
    if user is None:
        raise credentials_exception
    return user
        

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

router = APIRouter( 
    prefix="/token",
    tags = ['Authentication']
)

@router.post("/", response_model=schemas.Token)
async def login_for_access_token(user_credential:schemas.UserLogin, db: Session = Depends(get_db)):
    user = signup_route.verify_email(db,user_credential.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credential")

    elif not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid Credentials")
    
    elif not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_access_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )


    return {"access_token": access_token,
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES,
            "token_type":"bearer",
            "refresh_token":refresh_token}
'''

# router = APIRouter( 
#     prefix="/token",
#     tags = ['Authentication']
# )


# @router.post("/",response_model=schemas.NewToken)
# def create_access_token_from_refresh_token(x_token:str=Header):
#     payload = jwt.decode(x_token,REFRESH_SECRET_KEY,algorithms=[ALGORITHM])
#     new_access_token = create_access_token(data=payload)
#     return new_access_token
    
   


# def trial_decode(token:str):
#     payload = jwt.decode(token,REFRESH_SECRET_KEY,algorithms=[ALGORITHM])
#     print(payload)
#     print(type(payload))

# trial_decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2VtYWlsIjoidGVzdG93bmVyM0BnbWFpbC5jb20iLCJ1c2VyX3Bhc3N3b3JkIjoiJDJiJDEyJGh4UmJXbnNibVdQQlRRYlhFT1FuRE9NakJaQm05NE12NC9xRi9OQjZXTC5mS3NpamduUTlxIiwiZXhwIjoxNjcwMzMzNzg0fQ.VoBjz9qTBrZpH0AT5OZNEZCf5e6xLqPSVFoW_wiSNKk")
from typing import Union,Optional

## importing socket module
import socket
## getting the hostname by socket.gethostname() method
# hostname = socket.gethostname()
# ## getting the IP address using socket.gethostbyname() method
# ip_address = socket.gethostbyname(hostname)
# ## printing the hostname and ip_address
# print(f"Hostname: {hostname}")
# print(f"IP Address: {ip_address}")

device_id = "4C4C4544-0037-5010-8043-C6C04F564E32"

def create_session(user: schemas.UserLogin, db:Session,data:dict):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        device_id = "4C4C4544-0037-5010-8043-C6C04F564E32"
        db_session = models.Session(
                user_id = user.user_id,
                created_at = datetime.now(),
                logout_time= None,
                device_id = device_id,
                device_ip = ip_address,
                access_token = create_access_token(data),
                refresh_token= create_refresh_token(data),
                is_active = user.is_active
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        print(db_session)
        return {"access_token":db_session.access_token,
                "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES,
                 "token_type":"bearer",
                "refresh_token": db_session.refresh_token}


@router.post("/",status_code=status.HTTP_200_OK)
def login(user_credential:schemas.UserLogin, db: Session = Depends(get_db)):
    user = signup_route.verify_email(db,user_credential.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credential")

    elif not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid Credentials")
    
    # else:
    # # create token
    # # token_data = schemas.UserLogin
    #     # token_data = {"user_email":user.email,
    #     # "user_password":user.password}

    
    token_data = {"user_email":user.email}
    '''   
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    db_session = models.Session(
                user_id = user_credential.user_id,
                created_at = datetime.now(),
                logout_time= None,
                device_id = user_credential.device_id,
                device_ip = user_credential.device_ip,
                access_token = access_token,
                refresh_token= refresh_token,
                is_active = user_credential.is_active
        )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    # create_session(user_credential,db)
    return {"access_token":access_token,
                "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES,
                "token_type":"bearer",
                "refresh_token": refresh_token}
    '''
    session = create_session(user_credential,db,token_data)
    print(type(session))
    return session


    # for i,j in session.items():
    #     print(i,j)

        
    # return {"access_token":session,
    #             "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES,
    #             "token_type":"bearer",
    #             "refresh_token": session
    # }


    
# {
#     "user_id" : " ",
#     "created_at" : " ",
#     "logout_time": " ",
#     "device_id" : str,
#     "device_ip" : str,
#     "access_token" : str,
#     "refresh_token": str,
#     "is_active" : bool
# }

# def create_song(request: schemas.Song, db: Session = Depends(database.get_db)):
#             new_song = models.Song(name=request.name, duration=request.duration, uploadTime=request.uploadTime)
#             db.add(new_song)
#             db.commit()
#             db.refresh(new_song)
#             return new_song