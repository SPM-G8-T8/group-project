from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.sqlalchemy import paginate
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from schemas import (
    SkillDetailsRead,
    StaffSkillsRead,
    RoleSkillsRead,
    StaffSkillsCreate,
    StaffDetailsBase,
)
import models

router = APIRouter(prefix="/skill-match", tags=["skill_match"])

db_dependency = Annotated[Session, Depends(get_db)]


def calculate_matching_skills(staff_id: int, role_id: int, db: Session):
    staff_skills = (
        db.query(models.StaffSkills.skill_id)
        .filter(models.StaffSkills.staff_id == staff_id)
        .all()
    )
    role_skills = (
        db.query(models.RoleSkills.skill_id)
        .filter(models.RoleSkills.role_id == role_id)
        .all()
    )

    # check if staff_skills and role_skills are empty
    if not staff_skills and not role_skills:
        print(f"===== STAFF SKILLS DUMP {staff_skills} =====")
        print(f"===== ROLE SKILLS DUMP {role_skills} =====")

        return set(), set()

    staff_skills_set = set(skill[0] for skill in staff_skills)
    role_skills_set = set(skill[0] for skill in role_skills)

    matching_skills = staff_skills_set.intersection(role_skills_set)
    unmet_skills = staff_skills_set.difference(role_skills_set)
    unused_skills = role_skills_set.difference(staff_skills_set)

    return {
        "matching_skills": matching_skills,
        "unmet_skills": unmet_skills,
        "unused_skills": unused_skills,
    }


@router.get("/matching-percentage/{staff_id}/{role_id}")
async def get_matching_percentage(
    staff_id: int, role_id: int, db: Session = Depends(get_db)
):
    try:
        skill_match_dict = calculate_matching_skills(staff_id, role_id, db)
        matching_skills = skill_match_dict["matching_skills"]
        unmet_skills = skill_match_dict["unmet_skills"]
        unused_skills = skill_match_dict["unused_skills"]

        if len(matching_skills) + len(unmet_skills) == 0:
            return {
                "matching_percentage": 0,
                "unused_percentage": 0,
                "matched": [],
                "unmet": [],
            }

        matching_percentage = (
            len(matching_skills) / (len(matching_skills) + len(unmet_skills))
        ) * 100
        unused_percentage = (
            len(unused_skills) / (len(matching_skills) + len(unmet_skills))
        ) * 100

        response_data = {
            "matching_percentage": matching_percentage,
            "unused_percentage": unused_percentage,
            "matched": matching_skills,
            "unmet": unmet_skills,
            "unused": unused_skills,
        }

        response = {
            "status": 200,
            "message": "Successful matching",
            "data": response_data,
        }

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/findMatches/{role_id}", response_model=list[tuple])
async def get_top_candidates_by_listing(role_id: int, db: Session = Depends(get_db)):
    candidate_dict = {}
    all_staff = db.query(models.StaffDetails).all()

    for staff in all_staff:
        print(f"Staff Id: {staff.staff_id}, Role Id: {role_id}")
        res = await get_matching_percentage(
            staff.staff_id, role_id, db
        )  # Use await here
        print(f"res is type: {type(res)}")
        # check if res has a matching_percentage key
        if "matching_percentage" in res["data"]:
            print(res["data"]["matching_percentage"])
            candidate_dict[staff.staff_id] = res["data"]
        print("===== CANDIDATE DICT DUMP =====")
        print(candidate_dict)

    # sort the candidates by highest matching percentage ("matching_percentage") and then lowest unmet skills ("unmet_percentage")
    sorted_candidates = sorted(
        candidate_dict.items(),
        key=lambda x: (x[1]["matching_percentage"], x[1]["unused_percentage"]),
        reverse=True,
    )
    print(sorted_candidates)
    # Q: why is this a tuple?
    print(type(sorted_candidates[0]))

    # if sorted_candidates is >10, return the top 10
    return sorted_candidates[:10]
