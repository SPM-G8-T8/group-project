from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum
from typing import Union

class RoleListingBase(BaseModel):
    role_id: int
    role_listing_desc: str
    role_listing_source: int
    role_listing_open: date
    role_listing_close: date

class RoleListingCreate(RoleListingBase):
    role_listing_creator: int
    
class RoleListingUpdate(BaseModel):
    role_listing_desc: Union[str, None] = None
    role_listing_source: Union[int, None] = None
    role_listing_open: Union[date, None] = None
    role_listing_close: Union[date, None] = None


class RoleListingRead(RoleListingBase):
    role_listing_id: int
    role_listing_creator: int
    role_listing_updater: int
    role_listing_ts_create: datetime
    role_listing_ts_update: datetime
