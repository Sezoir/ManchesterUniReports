## Sqlalchemy libraries
# Core library
import sqlalchemy as db
# Orm library
import sqlalchemy.orm as orm
# Get the factory function for a Base class
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

## Math libraries
# Data frames
import pandas as pd
# General array math library
import numpy as np

## Env variables
import configparser

# @todo: find a way to include these variables as part of the class (Issue lies with declaration of base class)
# @todo: Test creation of engines with "try"
# @todo: https://stackoverflow.com/questions/4215920/how-to-bind-engine-when-i-want-when-using-declarative-base-in-sqlalchemy
# Set up config
config = configparser.ConfigParser()
config.read("settings.ini")
# Declare engine to sql server
engine = db.create_engine("mysql+pymysql://"+config.get("sql","username")+":"+config.get("sql","password")+"@"+config.get("sql","ip")+":"+config.get("sql","port")+"/"+config.get("sql","database"))
# Create base class using engine
Base = declarative_base(engine)
# Get metadata of the base
metadata = Base.metadata

# Define the jobs table
class Jobs(Base):
    # Define the sql table name
    __tablename__ = "jobs"
    # Set table parameters to autoload all variables from tables not explicitly defined
    __table_args__ = {'autoload': True}
    # Define column variables with foreign keys
    job_type = db.Column(db.Integer, db.ForeignKey("joboptions.id"), nullable=False)
    hazards = db.Column(db.Integer, db.ForeignKey("joboptions.id"), nullable=False)
    status = db.Column(db.Integer, db.ForeignKey("joboptions.id"), nullable=False)
    # Define the relationships between table variables
    rJob_type = orm.relationship("JobOptions", backref="jobs", foreign_keys=[job_type])
    rHazards = orm.relationship("JobOptions", foreign_keys=[hazards])
    rStatus = orm.relationship("JobOptions", foreign_keys=[status])
    rInternal = orm.relationship("Internal", uselist=False, lazy="joined", join_depth=1)
    rExternal = orm.relationship("External", uselist=False, lazy="joined", join_depth=1)
    rStandardJobType = orm.relationship("StandardJobType", uselist=False, lazy="joined", join_depth=1)
    rDesignJobType = orm.relationship("DesignJobType", uselist=False, lazy="joined", join_depth=1)
    # def __repr__(self):
    #     return "<internal(id=%s, %s)>" %(self.id, self.rInternal)

# Define the joboptions table
class JobOptions(Base):
    __tablename__ = "joboptions"
    __table_args__ = {'autoload': True}
    def __repr__(self):
        return "<internal(id=%s)>" %(self.id)

# Define the internal table
class Internal(Base):
    __tablename__ = "internal"
    __table_args__ = {'autoload': True}
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    building_id = db.Column(db.Integer, db.ForeignKey("joboptions.id"))
    staff_type_id = db.Column(db.Integer, db.ForeignKey("joboptions.id"))
    school_id = db.Column(db.Integer, db.ForeignKey("joboptions.id"))
    booked_by = db.Column(db.String, db.ForeignKey("usercache.username"))
    rBuilding = orm.relationship("JobOptions",  foreign_keys=[building_id], lazy="subquery")
    rStaffType = orm.relationship("JobOptions", foreign_keys=[staff_type_id], lazy="subquery")
    rSchool = orm.relationship("JobOptions", foreign_keys=[school_id], lazy="subquery")
    rBookedBy = orm.relationship("UserCache", foreign_keys=[booked_by], lazy="subquery")

# Define the external table
class External(Base):
    __tablename__ = "external"
    __table_args__ = {'autoload': True}
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    rCompany = orm.relationship("Companies")

# Define the standardjobtype table
class StandardJobType(Base):
    __tablename__ = "standardjobtype"
    __table_args__ = {'autoload': True}
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    assigned_user = db.Column(db.String, db.ForeignKey("usercache.username"))
    location = db.Column(db.Integer, db.ForeignKey("joboptions.id"))
    rAssignedUser = orm.relationship("UserCache", foreign_keys=[assigned_user], lazy="subquery")
    rLocation = orm.relationship("JobOptions", foreign_keys=[location], lazy="subquery")

# Define the designjobtype table
class DesignJobType(Base):
    __tablename__ = "designjobtype"
    __table_args__ = {'autoload': True}
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    design_user = db.Column(db.String, db.ForeignKey("usercache.username"))
    constructor_user = db.Column(db.String, db.ForeignKey("usercache.username"))
    rDesignUser = orm.relationship("UserCache", foreign_keys=[design_user], lazy="subquery")
    rConstructorUser = orm.relationship("UserCache", foreign_keys=[constructor_user], lazy="subquery")

# Define the usercache table
class UserCache(Base):
    __tablename__ = "usercache"
    __table_args__ = {'autoload': True}
    school_id = db.Column(db.Integer, db.ForeignKey("joboptions.id"))
    rSchoolId = orm.relationship("JobOptions", foreign_keys=[school_id], lazy="subquery")

# Define the companies table
class Companies(Base):
    __tablename__ = "companies"
    __table_args__ = {'autoload': True}


'''
# Repository class
# Used to query the database, and return the linked tables of data in a pandas dataframe.
'''
class Repository:
    def __init__(self):
        self.updTables()

    def updTables(self):
        # Create a session
        session = orm.Session(bind=engine)

        # Query for all jobs which have been successfully completed (that is not deleted, and not ongoing)
        query = session.query(Jobs).filter(db.and_(Jobs.completed_time.isnot(None), Jobs.deleted_at.is_(None))).all()

        # for row in query:
        #     print(row.id)

        # Iterate through each job, and add to list of dictionaries
        # (Note that adding to list of dict, then creating a dataframe from it is faster than using append)
        rowLists = []
        for row in query:
            # Create empty dict
            rowDict = {}
            # Update row dict with columns from jobs table
            rowDict.update({"id":row.id, "job_type":row.rJob_type.label, "hazards":row.rHazards.label,
                            "status":row.rStatus.label, "man_hours":row.man_hours, "pph":row.pph,
                            "consumables":row.consumables, "completed_time":row.completed_time,
                            "created_at":row.created_at})

            # Update row dict with columns from internal table if applicable
            internal = row.rInternal
            if internal != None:
                rowDict.update({"internal":True, "building_id":internal.rBuilding.label, "staff_type_id":internal.rStaffType.label,
                                "school_id":internal.rSchool.label, "booked_by_username": internal.booked_by,
                                "booked_by_first_name": internal.rBookedBy.first_name, "booked_by_last_name": internal.rBookedBy.last_name,
                                "booked_by_school_id":internal.rBookedBy.rSchoolId.label})
            else: rowDict.update({"internal":False})

            # Update row dict with columns from external table if applicable
            external = row.rExternal
            if external != None:
                rowDict.update({"external": True, "company_name":external.rCompany.company_name,
                                "company_address":external.rCompany.company_address})
            else:
                rowDict.update({"external": False})

            # Update row dict with columns from standardjobtype table if applicable
            standardjobtype = row.rStandardJobType
            if standardjobtype != None:
                rowDict.update({"standardjobtype": True, "equitment":standardjobtype.equitment,
                                "assigned_user_username":standardjobtype.rAssignedUser.username,
                                "assigned_user_first_name":standardjobtype.rAssignedUser.first_name,
                                "assigned_user_last_name":standardjobtype.rAssignedUser.last_name,
                                "location":standardjobtype.rLocation.label, "number_items":standardjobtype.number_items})
            else:
                rowDict.update({"standardjobtype": False})

            # Update row dict with columns from designjobtype table if applicable
            designjobtype = row.rDesignJobType
            if designjobtype != None:
                rowDict.update({"designjobtype": True, "title":designjobtype.title,
                                "design_user_username":designjobtype.rDesignUser.username,
                                "design_user_first_name":designjobtype.rDesignUser.first_name,
                                "design_user_last_name":designjobtype.rDesignUser.last_name,
                                "constructor_user_username": designjobtype.rConstructorUser.username,
                                "constructor_user_first_name": designjobtype.rConstructorUser.first_name,
                                "constructor_user_last_name": designjobtype.rConstructorUser.last_name})
            else:
                rowDict.update({"designjobtype": False})

            # Append rowDict to the list of dicts
            rowLists.append(rowDict)

        # Create dataframe based on dict
        self.mJobs = pd.DataFrame(rowLists)
        # Sort the dataframe based on the job id
        self.mJobs.sort_values(by=['id'], ascending=True, inplace=True)
        # Set the job id as the index
        self.mJobs.set_index('id', inplace=True)
        # Set any NaN types in the number_items column to 0
        self.mJobs.loc[self.mJobs.number_items.isna(),"number_items"] = 0
        # Clone any jobs based on the number_items @todo: change to not copy
        self.mJobs = self.mJobs.loc[self.mJobs.index.repeat(self.mJobs.number_items)]
        return

    mJobs = None