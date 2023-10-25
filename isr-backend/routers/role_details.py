from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated, List
from schemas import RoleDetails
import models

router = APIRouter(
    prefix='/roles',
    tags=['roles']
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/", response_model=List[RoleDetails])
def get_all_roles(db: db_dependency):

    try:
        res = db.query(models.RoleDetails).all()

        return res
    
    except SQLAlchemyError as e:
        return HTTPException(status_code=500, detail="Error retrieving roles")
    
@router.get("/{role_id}", response_model=RoleDetails)
def get_role(role_id: int, db: db_dependency):
    role = db.query(models.RoleDetails).filter(models.RoleDetails.role_id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role