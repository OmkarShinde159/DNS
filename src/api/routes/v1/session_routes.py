
from src.database.schemas import schemas
from src.database import models
from fastapi import status,HTTPException,Depends,APIRouter
from src.database.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from src.utils import utils
from src.api.routes.v1 import login_auth_routes as l

# method ----------------------------------------------------------------------------------------------------
def create_user_sesion(session:schemas.SessionBase,db:Session = Depends(get_db)):
    new = models.Session(**session.dict(), user_id=id)
    print(new)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new



