from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.encoders import jsonable_encoder
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated, List
from schemas import (
    StaffRolesRead,
    StaffDetailsBase,
    StaffSkillsRead,
    StaffSkillsUpdate,
    StaffReportingOfficerRead,
)
import models
from services import file_services
from pathlib import Path


router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/all-staff")
def get_all_staff(db: db_dependency):
    return db.query(models.StaffDetails).all()


@router.get("/staff-roles/{staff_id}", response_model=List[StaffRolesRead])
def get_staff_roles(staff_id: int, db: db_dependency):
    staff_roles = (
        db.query(models.StaffRoles)
        .join(models.RoleDetails)
        .filter(
            models.StaffRoles.staff_id == staff_id,
            models.StaffRoles.sr_status == "active",
        )
        .all()
    )

    if not staff_roles:
        raise HTTPException(status_code=404, detail="Staff roles not found")
    return staff_roles


@router.get("/staff-ro/{staff_id}", response_model=StaffReportingOfficerRead)
def get_staff_ro(staff_id: int, db: db_dependency):
    staff_ro = (
        db.query(models.StaffReportingOfficer)
        .filter(
            models.StaffReportingOfficer.staff_id == staff_id,
        )
        .first()
    )
    if not staff_ro:
        raise HTTPException(status_code=404, detail="Staff RO not found")
    return staff_ro


@router.get("/staff-skills/{staff_id}", response_model=List[StaffSkillsRead])
def get_staff_skills(staff_id: int, db: db_dependency):
    staff_skills = db.query(models.StaffSkills).filter(
        models.StaffSkills.staff_id == staff_id
    )
    if not staff_skills:
        raise HTTPException(status_code=404, detail="Staff skills not found")
    return staff_skills


@router.get("/staff-skills-sbrp/{staff_id}", response_model=List[StaffSkillsRead])
def get_staff_skills_sbrp(staff_id: int, db: db_dependency):
    staff_skills = (
        db.query(models.StaffSkillsSBRP)
        .join(models.SkillDetails)
        .filter(models.StaffSkillsSBRP.staff_id == staff_id)
    )
    if not staff_skills:
        raise HTTPException(status_code=404, detail="Staff skills (SBRP) not found")
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


@router.get("/staff/{staff_id}", response_model=StaffDetailsBase)
def get_one_staff_details(staff_id: int, db: db_dependency):
    staff_details = (
        db.query(models.StaffDetails)
        .filter(models.StaffDetails.staff_id == staff_id)
        .first()
    )
    if not staff_details:
        raise HTTPException(status_code=404, detail="Staff details not found")
    return staff_details


@router.post("/staff-skills/upload-cert/")
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
            certification_name=form["certification_name"],
            certifying_agency=form["certifying_agency"],
            certification_date=form["certification_date"],
            awardee_name=form["awardee_name"],
            file_name=new_file_name,
        )

        if file_services.upload_file(
            file=file.file, bucket="spm-proj-bucket", file_name=new_file_name
        ):
            existing_staff_skills_cert = (
                db.query(models.StaffSkillsCert)
                .filter(
                    models.StaffSkillsCert.staff_id == staff_id,
                    models.StaffSkillsCert.skill_id == skill_id,
                )
                .first()
            )
            if existing_staff_skills_cert:
                existing_staff_skills_cert.certifying_agency = form["certifying_agency"]
                existing_staff_skills_cert.certification_name = form[
                    "certification_name"
                ]
                existing_staff_skills_cert.awardee_name = form["awardee_name"]
                existing_staff_skills_cert.certification_date = form[
                    "certification_date"
                ]
                existing_staff_skills_cert.file_name = new_file_name
            else:
                db_staff_skills_sbrp = models.StaffSkillsSBRP(
                    staff_id=staff_id, skill_id=skill_id, ss_status="unverified"
                )
                db.add(db_staff_skills_cert)
                db.add(db_staff_skills_sbrp)

            db.commit()

            return {"message": "Certification uploaded successfully"}
        else:
            return {"message": "error"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/staff-skills/add/{staff_id}/{skill_id}")
def add_skill(staff_id: int, skill_id: int, db: db_dependency):
    try:
        db_staff_skills_sbrp = models.StaffSkillsSBRP(
            staff_id=staff_id, skill_id=skill_id, ss_status="unverified"
        )
        db.add(db_staff_skills_sbrp)
        db.commit()
        return {"message": "Skill added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/staff-skills/get-cert/{staff_id}/{skill_id}")
async def get_cert(db: db_dependency, staff_id: int, skill_id: int):
    cert_details = (
        db.query(models.StaffSkillsCert)
        .filter_by(staff_id=staff_id, skill_id=skill_id)
        .first()
    )

    if cert_details is None:
        raise HTTPException(status_code=404, detail="Certification not found")
    else:
        object_key = cert_details.file_name

    if not file_services.key_exists(object_key):
        raise HTTPException(status_code=404, detail="File not found")

    else:
        response = file_services.fetch_file(object_key)
        return response
