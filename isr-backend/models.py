from sqlalchemy import Column, ForeignKey, String, Integer, Date, DateTime, Enum
from sqlalchemy.sql import func
from database import Base

from sqlalchemy.orm import relationship

class StaffDetails(Base):
    __tablename__ = 'staff_details'

    staff_id = Column(Integer, primary_key=True)
    staff_fname = Column(String(50), nullable=False)
    staff_lname = Column(String(50), nullable=False)
    dept = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(20))
    biz_address = Column(String(255))
    sys_role = Column(Enum("staff", "hr", "manager", "inactive", name="sys_role_enum"))


class SkillDetails(Base):
    __tablename__ = 'skill_details'

    skill_id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(50), nullable=False)
    skill_status = Column(Enum("active", "inactive", name="skill_status_enum"))


class RoleDetails(Base):
    __tablename__ = 'role_details'

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), nullable=False)
    role_description = Column(String(50000))
    role_status = Column(Enum("active", "inactive", name="role_status_enum"))


class RoleSkills(Base):
    __tablename__ = 'role_skills'

    role_id = Column(Integer, primary_key=True)
    skill_id = Column(Integer, primary_key=True)



class StaffReportingOfficer(Base):
    __tablename__ = 'staff_reporting_officer'

    staff_id = Column(Integer, primary_key=True)
    RO_id = Column(Integer, primary_key=True)


class StaffRoles(Base):
    __tablename__ = 'staff_roles'

    staff_id = Column(Integer, primary_key=True)
    staff_role = Column(Integer, ForeignKey(RoleDetails.role_id))
    role_type = Column(Enum("primary", "secondary", name="role_type_enum"))
    sr_status = Column(Enum("active", "inactive", name="sr_status_enum"))


class StaffSkills(Base):
    __tablename__ = 'staff_skills'

    staff_id = Column(Integer, primary_key=True)
    skill_id = Column(Integer, nullable=False)
    ss_status = Column(Enum("active", "unverified", "in-progress", name="ss_status_enum"))

class RoleListings(Base):
    __tablename__ = 'role_listings'

    role_listing_id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey(RoleDetails.role_id))
    role_listing_desc = Column(String(50000))
    role_listing_source = Column(Integer, ForeignKey(StaffDetails.staff_id))
    role_listing_open = Column(Date)
    role_listing_close = Column(Date)
    role_listing_creator = Column(Integer, ForeignKey(StaffDetails.staff_id))
    role_listing_updater = Column(Integer, ForeignKey(StaffDetails.staff_id))
    role_listing_ts_create = Column(DateTime(timezone=True), server_default=func.now())
    role_listing_ts_update = Column(DateTime(timezone=True), onupdate=func.now())

    role = relationship("RoleDetails", backref="role_listings")

class RoleApplications(Base):
    __tablename__ = 'role_applications'

    role_app_id = Column(Integer, primary_key=True, index=True)
    role_listing_id = Column(Integer)
    staff_id = Column(Integer)
    role_app_ts_create = Column(DateTime(timezone=True), server_default=func.now())
    role_app_status = Column(Enum("applied", "withdrawn", name="role_app_enum"))







