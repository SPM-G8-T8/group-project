from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.sqlalchemy import paginate
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated, List
from schemas import StaffRolesRead, StaffDetailsBase, StaffSkillsRead, StaffSkillsUpdate
import models

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/staff-roles/{staff_id}", response_model=StaffRolesRead)
def get_staff_roles(staff_id: int, db: db_dependency):
    staff_roles = db.query(models.StaffRoles).filter(models.StaffRoles.staff_id == staff_id, 
                                                     models.StaffRoles.sr_status == "active").all()
    if not staff_roles:
        raise HTTPException(status_code=404, detail="Staff roles not found")
    return staff_roles

@router.get("/staff-skills/{staff_id}", response_model=List[StaffSkillsRead])
def get_staff_skills(staff_id: int, db: db_dependency):
    staff_skills = db.query(models.StaffSkills).join(models.SkillDetails).filter(models.StaffSkills.staff_id == staff_id)
    if not staff_skills:
        raise HTTPException(status_code=404, detail="Staff skills not found")
    return staff_skills

@router.get("/staff/", response_model=StaffDetailsBase)
def get_staff_details(staff_email: str, db: db_dependency):
    print(f"===== STAFF EMAIL {staff_email} =====")
    staff_details = db.query(models.StaffDetails).filter(models.StaffDetails.email == staff_email).first()
    if not staff_details:
        raise HTTPException(status_code=404, detail="Staff details not found")
    return staff_details

@router.put("/staff-skills/update/{staff_id}", response_model=List[StaffSkillsUpdate])
def update_staff_skills(staff_id: int, updatedSkills: StaffSkillsUpdate, db: db_dependency):
    try:
        staff_skills = db.query(models.StaffSkills).join(models.SkillDetails).filter(models.StaffSkills.staff_id == staff_id)
        if not staff_skills:
            raise HTTPException(status_code=404, detail="Staff skills not found")
        db_staff_skills.staff_id = updatedSkills.staff_id
        db_staff_skills.skill_id = updatedSkills.skill_id
        db_staff_skills.ss_status = updatedSkills.ss_status
        db_staff_skills.skill = updatedSkills.skill
        db.commit()
        return {"message": "Staff Skill updated", "skill": jsonable_encoder(db_staff_skills)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))