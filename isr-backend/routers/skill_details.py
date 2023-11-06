from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
import json
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated, List
from schemas import SkillDetailsRead, SkillDetailsCreate, SkillDetailsUpdate
import models

router = APIRouter(prefix="/skills", tags=["skills_details"])

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=List[SkillDetailsRead])
def get_all_skills(
    db: db_dependency, skill_id: int | None = None, filter: str | None = None
):
    res = db.query(models.SkillDetails)
    if filter:
        res = res.filter(models.SkillDetails.skill_name.contains(filter))
    if res.count() == 0:
        raise HTTPException(status_code=404, detail="No skills found")
    return res

@router.get("/byName", response_model=SkillDetailsRead)
def get_skill_by_name(skill_name: str, db: db_dependency):
    res = (
        db.query(models.SkillDetails)
        .filter(models.SkillDetails.skill_name == skill_name)
        .first()
    )
    if not res:
        raise HTTPException(status_code=404, detail="Skill not found")
    return res


@router.get("/{skill_id}", response_model=SkillDetailsRead)
def get_skill_by_id(skill_id: int, db: db_dependency):
    res = (
        db.query(models.SkillDetails)
        .filter(models.SkillDetails.skill_id == skill_id)
        .first()
    )
    if not res:
        raise HTTPException(status_code=404, detail="Skill not found")
    return res


@router.delete("/deleteSkill/{skill_id}")
def delete_skill(skill_id: int, db: db_dependency):
    db_skill = (
        db.query(models.SkillDetails)
        .filter(models.SkillDetails.skill_id == skill_id)
        .first()
    )
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    try:
        db.delete(db_skill)
        db.commit()
        return {
            "message": "Skill deleted",
            "skill": jsonable_encoder(db_skill.to_dict()),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create")
def create_skill(skill: SkillDetailsCreate, db: db_dependency):
    try:
        db_skill = models.SkillDetails(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            skill_status=skill.skill_status,
        )
        db.add(db_skill)
        db.commit()

        return {
            "message": "Skill created",
            "skill": jsonable_encoder(db_skill.to_dict()),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/editSkill/{skill_id}")
def update_skill(skill_id: int, skill: SkillDetailsUpdate, db: db_dependency):
    db_skill = (
        db.query(models.SkillDetails)
        .filter(models.SkillDetails.skill_id == skill_id)
        .first()
    )
    print("---- print db_skill ----")
    print(db_skill is None)
    print(type(db_skill))
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    try:
        if skill.skill_name is not None:
            db_skill.skill_name = skill.skill_name
        if skill.skill_status is not None:
            db_skill.skill_status = skill.skill_status

        db.commit()
        print(f"+==== DB SKILL: {db_skill.to_dict()} ===+")
        return {
            "status": 200,
            "message": "Skill updated",
            "skill": jsonable_encoder(db_skill.to_dict()),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
