from src.database.schemas import schemas
from src.database import models
from fastapi import status,HTTPException,Depends,APIRouter
from src.database.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from src.utils import utils
from src.api.routes.v1 import login_auth_routes as auth
from typing import Optional


router = APIRouter(
    prefix="/logout",
    tags = ['Users']
)

@router.get("/", response_model=list[schemas.UserOut])
def get_post(db: Session = Depends(get_db),
    current_user: int = Depends(auth.get_current_user),limit: int=10,skip:int=0,search:Optional[str]=""):

    posts = db.query(models.User).all()
    # print(results)
    return posts
