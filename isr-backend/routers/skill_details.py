from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi.encoders import jsonable_encoder
from database import get_db, SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from schemas import SkillDetailsRead, SkillDetailsCreate, SkillDetailsUpdate
import models
import json

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/skills", response_model=Page[SkillDetailsRead])
def get_all_skills(db: db_dependency, skill_id: int | None = None, filter: str | None = None):
    res = db.query(models.SkillDetails)
    if filter:
        res = res.filter(models.SkillDetails.skill_name.contains(filter))
    if res.count() == 0:
        raise HTTPException(status_code=404, detail="No skills found")
    return paginate(res)

@router.get("/skills/{skill_id}", response_model=SkillDetailsRead)
def get_skill_by_id(skill_id: int, db: db_dependency):
    res = db.query(models.SkillDetails).filter(models.SkillDetails.skill_id == skill_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Skill not found")
    return res

@router.post("/skills/create")
def create_skill(skill: SkillDetailsCreate, db: db_dependency):
    try:
        db_skill = models.SkillDetails(
            skill_id=skill.skill_id, 
            skill_name=skill.skill_name, 
            skill_status=skill.skill_status
        )
        db.add(db_skill)
        db.commit()

        return {"message": "Skill created", "skill": jsonable_encoder(db_skill)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/skills/{skill_id}")
def update_skill(skill_id: int, skill: SkillDetailsUpdate, db: db_dependency):
    try:
        db_skill = db.query(models.SkillDetails).filter(models.SkillDetails.skill_id == skill_id).first()
        if not db_skill:
            raise HTTPException(status_code=404, detail="Skill not found")
        db_skill.skill_name = skill.skill_name
        db_skill.skill_status = skill.skill_status
        db.commit()
        return {"message": "Skill updated", "skill": jsonable_encoder(db_skill)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
