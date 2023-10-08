from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum
from typing import Optional, Union


class RoleDetails(BaseModel):
    role_id: int
    role_name: str
    role_description: str
    role_status: str

class RoleListingBase(BaseModel):
    role_id: int
    role_listing_desc: str
    role_listing_source: int
    role_listing_open: date
    role_listing_close: date

class RoleListingCreate(RoleListingBase):
    role_listing_id: int
    role_listing_creator: int
    
class RoleListingUpdate(BaseModel):
    role_listing_desc: Union[str, None] = None
    role_listing_source: Union[int, None] = None
    role_listing_open: Union[date, None] = None
    role_listing_close: Union[date, None] = None

class RoleListingRead(RoleListingBase):
    role_listing_id: int
    role_listing_creator: int
    role_listing_updater: Optional[int]
    role_listing_ts_create: datetime
    role_listing_ts_update: Optional[datetime]
    role: RoleDetails

class SkillDetailsBase(BaseModel):
    skill_id: int
    skill_name: str
    skill_status: str

class SkillDetailsCreate(SkillDetailsBase):
    pass

class SkillDetailsUpdate(SkillDetailsBase):
    pass

class SkillDetailsRead(SkillDetailsBase):
    pass

class StaffSkillsBase(BaseModel):
    staff_id: int
    skill_id: int
    ss_status: str

class StaffSkillsCreate(StaffSkillsBase):
    pass

class StaffSkillsUpdate(StaffSkillsBase):
    pass

class StaffSkillsRead(StaffSkillsBase):
    class Config:
        orm_mode = True

class RoleSkillsRead(BaseModel):
    role_id: int
    skill_id: int

class RoleApplicationsBase(BaseModel):
    role_app_id: int
    role_listing_id: int
    staff_id: int
    role_app_status: str
    role_app_ts_create: datetime

class RoleApplicationsRead(RoleApplicationsBase):
    pass

class StaffDetailsBase(BaseModel):
    staff_id: int
    staff_fname: str
    staff_lname: str
    dept: str
    email: str
    phone: str
    biz_address: str
    sys_role: str

class StaffDetailsRead(StaffDetailsBase):
    pass