from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
import models
from database import get_db, engine
from sqlalchemy.orm import Session
from typing import Annotated

from routers import role_listing, skill_details, role_application

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db_dependency = Annotated[Session, Depends(get_db)]
models.Base.metadata.create_all(bind=engine)

app.include_router(role_listing.router)
app.include_router(skill_details.router)
app.include_router(role_application.router)


add_pagination(app)

