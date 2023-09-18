from sqlalchemy import Column, ForeignKey, BigInteger, String, Integer, Date, DateTime
from sqlalchemy.sql import func
from database import Base


class RoleListings(Base):
    __tablename__ = 'role_listings'

    role_listing_id = Column(BigInteger, primary_key=True, index=True)
    role_id = Column(BigInteger, ForeignKey("role_details.role_id"))
    role_listing_desc = Column(String)
    role_listing_source = Column(Integer, ForeignKey("staff_details.staff_id"))
    role_listing_open = Column(Date)
    role_listing_close = Column(Date)
    role_listing_creator = Column(Integer, ForeignKey("staff_details.staff_id"))
    role_listing_updater = Column(Integer, ForeignKey("staff_details.staff_id"))
    role_listing_ts_create = Column(DateTime(timezone=True), server_default=func.now())
    role_listing_ts_update = Column(DateTime(timezone=True), onupdate=func.now())


class RoleApplications(Base):
    __tablename__ = 'role_applications'

    role_app_id = Column(BigInteger, primary_key=True, index=True)
    role_listing_id = Column(BigInteger)
    staff_id = Column(BigInteger)
    role_app_ts_create = Column(DateTime(timezone=True), server_default=func.now())
    role_app_status = Column()


class RoleDetails(Base):
    __tablename__ = 'role_details'

    role_id = Column(BigInteger, primary_key=True, index=True)
    role_name = Column(String, nullable=False)
    role_description = Column(String)
    role_status = Column()


class RoleSkills(Base):
    __tablename__ = 'role_skills'

    role_id = Column(BigInteger, primary_key=True, index=True)
    skill_id = Column(BigInteger, primary_key=True, index=True)


class SkillDetails(Base):
    __tablename__ = 'skill_details'

    skill_id = Column(BigInteger, primary_key=True, index=True)
    skill_name = Column(String, nullable=False)
    skill_status = Column()


class StaffDetails(Base):
    __tablename__ = 'staff_details'

    staff_id = Column(BigInteger, primary_key=True)
    staff_fname = Column(String, nullable=False)
    staff_lname = Column(String, nullable=False)
    dept = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    biz_address = Column(String)
    sys_role = Column()


class StaffReportingOfficer(Base):
    __tablename__ = 'staff_reporting_officer'

    staff_id = Column(BigInteger, primary_key=True)
    RO_id = Column(BigInteger, ForeignKey("staff_details.staff_id"))


class StaffRoles(Base):
    __tablename__ = 'staff_roles'

    staff_id = Column(BigInteger, primary_key=True)
    staff_role = Column(BigInteger, ForeignKey("role_details.role_id"))
    role_type = Column()
    sr_status = Column()


class StaffSkills(Base):
    __tablename__ = 'staff_skills'

    staff_id = Column(BigInteger, primary_key=True)
    skill_id = Column(BigInteger, nullable=False)
    ss_status = Column()