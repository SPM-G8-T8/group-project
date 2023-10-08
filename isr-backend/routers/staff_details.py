from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.sqlalchemy import paginate
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from schemas import StaffRolesRead, StaffSkillsBase
import models

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/staff-roles/{staff_id}", response_model=Page[StaffRolesRead])
def get_staff_roles(staff_id: int, db: db_dependency):
    staff_roles = db.query(models.StaffRoles).filter(models.StaffRoles.staff_id == staff_id, 
                                                     models.StaffRoles.sr_status == "active").all()
    if not staff_roles:
        raise HTTPException(status_code=404, detail="Staff roles not found")
    return paginate(staff_roles)

@router.get("/staff-skills/{staff_id}", response_model=Page[StaffSkillsBase])
def get_staff_skills(staff_id: int, db: db_dependency):
    staff_skills = db.query(models.StaffSkills).filter(models.StaffSkills.staff_id == staff_id)
    if not staff_skills:
        raise HTTPException(status_code=404, detail="Staff skills not found")
    return paginate(staff_skills)

