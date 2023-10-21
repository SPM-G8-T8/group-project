from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.sqlalchemy import paginate
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated, List
from schemas import StaffRolesRead, StaffDetailsBase, StaffSkillsRead, StaffSkillsUpdate
import models
from services import file_services
from fastapi import File, UploadFile
import boto3
import os
from pathlib import Path


router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/staff-roles/{staff_id}", response_model=StaffRolesRead)
def get_staff_roles(staff_id: int, db: db_dependency):
    staff_roles = (
        db.query(models.StaffRoles)
        .filter(
            models.StaffRoles.staff_id == staff_id,
            models.StaffRoles.sr_status == "active",
        )
        .all()
    )
    if not staff_roles:
        raise HTTPException(status_code=404, detail="Staff roles not found")
    return staff_roles


@router.get("/staff-skills/{staff_id}", response_model=List[StaffSkillsRead])
def get_staff_skills(staff_id: int, db: db_dependency):
    staff_skills = (
        db.query(models.StaffSkills)
        .join(models.SkillDetails)
        .filter(models.StaffSkills.staff_id == staff_id)
    )
    if not staff_skills:
        raise HTTPException(status_code=404, detail="Staff skills not found")
    return staff_skills


@router.get("/staff/", response_model=StaffDetailsBase)
def get_staff_details(staff_email: str, db: db_dependency):
    print(f"===== STAFF EMAIL {staff_email} =====")
    staff_details = (
        db.query(models.StaffDetails)
        .filter(models.StaffDetails.email == staff_email)
        .first()
    )
    if not staff_details:
        raise HTTPException(status_code=404, detail="Staff details not found")
    return staff_details


@router.put("/staff-skills/update/{staff_id}", response_model=List[StaffSkillsUpdate])
def update_staff_skills(
    staff_id: int, updatedSkills: StaffSkillsUpdate, db: db_dependency
):
@router.put("/staff-skills/update/{staff_id}/{skill_id}/{skill_status}")
def update_staff_skills(staff_id: int, skill_id: int, skill_status: str, db: db_dependency):

    try:
        staff_skills = (
            db.query(models.StaffSkills)
            .join(models.SkillDetails)
            .filter(models.StaffSkills.staff_id == staff_id)
        )
        staff_skills = db.query(models.StaffSkills).filter(models.StaffSkills.staff_id == staff_id, models.StaffSkills.skill_id == skill_id).first()

        if not staff_skills:
            raise HTTPException(status_code=404, detail="Staff skills not found")
        db_staff_skills.staff_id = updatedSkills.staff_id
        db_staff_skills.skill_id = updatedSkills.skill_id
        db_staff_skills.ss_status = updatedSkills.ss_status
        db_staff_skills.skill = updatedSkills.skill
        db.commit()
        return {
            "message": "Staff Skill updated",
            "skill": jsonable_encoder(db_staff_skills),
        }
        return {"message": "Staff Skils updated", "skill": staff_skills}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/staff-skills/upload_cert/")
async def upload_cert(db: db_dependency, request: Request):
    try:
        form = await request.form()
        file = form["file"]
        staff_id = form["staff_id"]
        skill_id = form["skill_id"]

        original_filename = Path(file.filename)
        new_file_name = f"{staff_id}_{skill_id}{original_filename.suffix}"

        db_staff_skills_cert = models.StaffSkillsCert(
            staff_id=staff_id,
            skill_id=skill_id,
            certification_name = form["certification_name"]
            certifying_agency = form["certifying_agency"]
            certification_date = form["certification_date"]
            awardee_name = form["awardee_name"]
            file_name=new_file_name
        )

        db.add(db_staff_skills_cert)
        db.commit()

        file_services.upload_file(
            file=file.file, bucket="spm-proj-bucket", file_name=new_file_name
        )
        return {"message": "Certification uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/staff-skills/get_cert/{object_key}")
async def get_cert(object_key: str):
    try:
        response = file_services.fetch_file(object_key)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
