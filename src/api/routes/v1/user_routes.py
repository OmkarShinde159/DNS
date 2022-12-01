from src.database.schemas import schemas
from src.database import models
from fastapi import status,HTTPException,Depends,APIRouter
from src.database.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID


router = APIRouter(
    prefix="/signup",
    tags = ['Users']
)

# methods ------------------------------------------------------------------------------

def get_user(db: Session, user_id: UUID):
    ''' get user by user_id'''
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    '''get user by email'''
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    '''get all users'''
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash(user.password)
    user.password = hashed_password
    db_user = models.User(**user.dict())
    print(db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# routes --------------------------------------------------------------------

@router.post("/",response_model=schemas.UserOut,)
def user_signup(user:schemas.UserCreate, db:Session=Depends(get_db)):
    if get_user_by_email(db,user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email Already Exists")
        
    return create_user(db=db, user=user)


   

