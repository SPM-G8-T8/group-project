from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi.encoders import jsonable_encoder
from database import get_db, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
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


@router.get("/", response_model=Page[RoleListingRead])
def get_all_listings(db: db_dependency, listing_id: int | None = None, filter: str | None = None):
    
    res = db.query(models.RoleListings) \
    .join(models.RoleDetails) \
    .filter(models.RoleDetails.role_status == "active",
            models.RoleDetails.role_id == models.RoleListings.role_id)
    if filter:
        res = res.filter(models.RoleListings.role_listing_desc.contains(filter))
    
    if res.count() == 0:
            raise HTTPException(status_code=404, detail="No listings found")     
    
    return paginate(res)


@router.get("/{listing_id}", response_model=RoleListingRead)
def get_listing_by_id(listing_id: int, db: db_dependency):
    
    res = db.query(models.RoleListings) \
    .join(models.RoleDetails) \
    .filter(models.RoleDetails.role_status == "active",
            models.RoleDetails.role_id == models.RoleListings.role_id,
            models.RoleListings.role_listing_id == listing_id).first()

    if not res:
        raise HTTPException(status_code=404, detail="Listing not found")

    return res


@router.post("/create")
def create_listings(listing: RoleListingCreate, db: db_dependency):

    listing_query = db.query(models.RoleListings).filter(models.RoleListings.role_listing_id == listing.role_listing_id).first()

    if listing_query:
        raise HTTPException(status_code=409, detail=f"Role Listing ID {listing.role_listing_id} already exist!")


    try: 
        listing_obj = models.RoleListings(
            role_listing_id = listing.role_listing_id,
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
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e.orig))


