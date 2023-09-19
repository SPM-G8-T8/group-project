from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
import models
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated

from routers import role_listing, skill_details

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


db_dependency = Annotated[Session, Depends(get_db)]


app.include_router(role_listing.router)
app.include_router(skill_details.router)


add_pagination(app)

@app.get("/test")
def test(db: db_dependency):
    res = db.query(models.SkillDetails).all()
    print(res)

    return res