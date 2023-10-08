from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi.encoders import jsonable_encoder
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Annotated, Optional
from schemas import RoleApplicationsBase, RoleApplicationCreate, RoleApplicationsRead
import models
import datetime
import json

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/application", response_model=Page[RoleApplicationsRead])
def get_all_applications(db: db_dependency, role_app_id: int | None = None, filter: str | None = None):
    res = db.query(models.RoleApplications)
    if res.count() == 0:
        raise HTTPException(status_code=404, detail="No applications found")
    return paginate(res)

@router.post("/application/create")
def create_application(application: RoleApplicationCreate, db: db_dependency):

    try:
        db_application = models.RoleApplications(
            role_app_id=application.role_app_id,
            role_listing_id=application.role_listing_id,
            staff_id=application.staff_id,
            role_app_ts_create=datetime.datetime.now(),
            role_app_status=application.role_app_status
        )
        db.add(db_application)
        db.commit()
        

        return {"message": "Application created", "application": jsonable_encoder(db_application)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))