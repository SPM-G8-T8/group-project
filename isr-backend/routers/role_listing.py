from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi.encoders import jsonable_encoder
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Annotated, Optional
from schemas import RoleListingCreate, RoleListingRead, RoleListingUpdate
import models
import datetime
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
def get_all_listings(db: db_dependency,  
                     filter: str | None = None,
                     hide_expired: Optional[bool] = True,
                     role_filter: Optional[int] = None
                     ):
    
    res = db.query(models.RoleListings) \
    .join(models.RoleDetails) \
    .filter(models.RoleDetails.role_status == "active",
            models.RoleDetails.role_id == models.RoleListings.role_id)
    
    if hide_expired:
        today = datetime.datetime.now().date()
        res = res.filter(models.RoleListings.role_listing_close >= today, models.RoleListings.role_listing_open <= today) 


    if filter:
        res = res.filter(models.RoleListings.role_listing_desc.contains(filter))

    if role_filter:
        res = res.filter(models.RoleListings.role_id == role_filter)

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

    if listing.role_listing_open > listing.role_listing_close:
         raise HTTPException(status_code=400, detail="Open Date must be before Close Date.")

    try: 
        listing_obj = models.RoleListings(**dict(listing))

        db.add(listing_obj)
        db.commit()

        return {"message": "Listing created!", "listing": jsonable_encoder(listing_obj)}
    
    except SQLAlchemyError as e:
        print(e)

        raise HTTPException(status_code=500, detail="Error creating listing! Please ensure the following are correct: <br>1. Role ID exists <br>2. Role Source exists <br>3. Role Listing ID is unique")
    
@router.put("/edit/{listing_id}")
def edit_listing(listing_id: int, listing: RoleListingUpdate, db: db_dependency,):
    res = db.query(models.RoleListings) \
        .join(models.RoleDetails) \
        .filter(models.RoleDetails.role_status == "active",
                models.RoleDetails.role_id == models.RoleListings.role_id,
                models.RoleListings.role_listing_id == listing_id).first()

    if not res:
        raise HTTPException(status_code=404, detail="Listing not found")
    else: 
        try:
            listing_data = listing.dict(exclude_unset=True)
            for key,value in listing_data.items():
                setattr(res, key,value)
            db.add(res)
            db.commit()

            return {"message": "Listing edited", "listing": jsonable_encoder(listing_data)}
        
        except SQLAlchemyError as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error editing listing! Please ensure the following are correct: <br>1. Role ID exists <br>2. Role Source exists <br>3. Role Listing ID is unique")
        

@router.patch("/deactivate/{listing_id}")
def deactivate_listing(listing_id: int, db: db_dependency):
    res = db.query(models.RoleListings).filter(models.RoleListings.role_listing_id == listing_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    try:
        res.role_listing_status = "inactive"
        db.commit()
        return Response(status_code=204)
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error deactivating listing")