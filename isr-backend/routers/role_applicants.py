from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.sqlalchemy import paginate
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from schemas import RoleApplicationCreate, RoleApplicationsRead, StaffDetailsRead
import models

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/applicants", response_model=Page[RoleApplicationsRead])
def get_all_applicants(db: db_dependency):
    res = db.query(models.RoleApplications).filter(models.RoleApplications.role_app_status == "applied")
    if res.count() == 0:
        raise HTTPException(status_code=404, detail="No applicants found")
    return paginate(res)


@router.get("/applicants/{role_listing_id}", response_model=Page[StaffDetailsRead])   
def get_applicants(role_listing_id: int, db: db_dependency):
    res = db.query(models.StaffDetails) \
    .join(models.RoleApplications, models.StaffDetails.staff_id == models.RoleApplications.staff_id) \
    .filter(models.RoleApplications.role_listing_id == role_listing_id,
            models.RoleApplications.role_app_status == "applied")
    if res.count() == 0:
        raise HTTPException(status_code=404, detail="No applicants found")
    return paginate(res)

@router.post("/applicants/create")
def create_application(application: RoleApplicationCreate, db: db_dependency):

    print(application)

    res = db.query(models.RoleApplications).filter(models.RoleApplications.role_listing_id == application.role_listing_id, models.RoleApplications.staff_id == application.staff_id)

    if res.count() > 0:
        raise HTTPException(status_code=409, detail="Application already exists")

    try:
        application_obj = models.RoleApplications(
            role_listing_id = application.role_listing_id,
            staff_id = application.staff_id,
            role_app_status = "applied",
        )

        db.add(application_obj)
        db.commit()

        return {"message": "Application created"}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))