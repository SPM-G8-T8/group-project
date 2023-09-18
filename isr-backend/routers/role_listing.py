from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from database import get_db, SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from schemas import RoleListingCreate, RoleListingRead, RoleListingUpdate
import models
import json


'''
prefix: adds a prefix in every decorator provided in this page
endpoint - localhost:3000/listing/...

tags: provides title for generated documentation
'''
router = APIRouter(
    prefix='/listing',
    tags=['role_listing']
)

db_dependency = Annotated[Session, Depends(get_db)]



@router.post("/create")
def create_listings(listing: RoleListingCreate, db: db_dependency):

    print(listing)

    try: 
        listing_obj = models.RoleListings(
            role_id = listing.role_id,
            role_listing_desc = listing.role_listing_desc,
            role_listing_source = listing.role_listing_source,
            role_listing_open = listing.role_listing_open,
            role_listing_close = listing.role_listing_close,
            role_listing_creator = listing.role_listing_creator
        )

        db.add(listing_obj)
        db.commit()

        return {"message": "Listing created!", "listing": jsonable_encoder(listing_obj)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def get_all_listings(db: db_dependency):
    res = db.query(models.RoleListings).all()

    return res