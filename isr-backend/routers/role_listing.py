from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


class RoleListing(BaseModel):
    pass








'''
prefix: adds a prefix in every decorator provided in this page
endpoint - localhost:3000/listing/...

tags: 
'''
router = APIRouter(
    prefix='/listing',
    tags=['role_listing']
)

@router.get("/test")
def test():
    return "Hello"
