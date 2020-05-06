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
    status = db.Column(db.Integer, db.ForeignKey("joboptions.id"), nullable = False)
    # Define the relationships between table variables
    rJob_type = orm.relationship("JobOptions", backref="jobs", foreign_keys=[job_type])
    rHazards = orm.relationship("JobOptions", foreign_keys=[hazards])
    rStatus = orm.relationship("JobOptions", foreign_keys=[status])
    rInternal = orm.relationship("Internal", uselist=False, back_populates="rJobs")
    def __repr__(self):
        return "<internal(id=%s, %s)>" %(self.id, self.rInternal)

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
    rBuilding = orm.relationship("JobOptions",  foreign_keys=[building_id])
    rStaffType = orm.relationship("JobOptions", foreign_keys=[staff_type_id])
    rSchool = orm.relationship("JobOptions", foreign_keys=[school_id])
    rBookedBy = orm.relationship("UserCache", foreign_keys=[booked_by])
    rJobs = orm.relationship("Jobs", back_populates="rInternal")

# Define the external table
class External(Base):
    __tablename__ = "external"
    __table_args__ = {'autoload': True}
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    rCompany = orm.relationship("Companies")
    rJobs = orm.relationship("Jobs")

# Define the standardjobtype table
class StandardJobType(Base):
    __tablename__ = "standardjobtype"
    __table_args__ = {'autoload': True}
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    assigned_user = db.Column(db.String, db.ForeignKey("usercache.username"))
    location = db.Column(db.Integer, db.ForeignKey("joboptions.id"))
    rAssignedUser = orm.relationship("UserCache", foreign_keys=[assigned_user])
    rLocation = orm.relationship("JobOptions", foreign_keys=[location])

# Define the designjobtype table
class DesignJobType(Base):
    __tablename__ = "designjobtype"
    __table_args__ = {'autoload': True}
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    design_user = db.Column(db.String, db.ForeignKey("usercache.username"))
    constructor_user = db.Column(db.String, db.ForeignKey("usercache.username"))
    rDesignUser = orm.relationship("UserCache", foreign_keys=[design_user])
    rConstructorUser = orm.relationship("UserCache", foreign_keys=[constructor_user])

# Define the usercache table
class UserCache(Base):
    __tablename__ = "usercache"
    __table_args__ = {'autoload': True}

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
        # Get a dataframe from the jobs table with table links, and set the index to the job id
        self.mJobs = self.updTable(Jobs,
                      columns=["id", "job_number", "clone_from", "man_hours", "pph", "consumables", "completed_time", "created_at", "updated_at", "deleted_at"],
                      relColumns={"rJob_type":[["label"], ["jobType"]], "rHazards":[["label"], ["hazards"]], "rStatus":[["label"], ["status"]]}).set_index("id")
        # All other tables refer to the jobs.id as job_id, so we change the index name
        self.mJobs.index.name = "job_id"
        # Get the dataframe for external table with table links
        external = self.updTable(External,
                                 columns=["job_id"], relColumns={"rCompany":[["company_name"], ["companyName"]]}).set_index("job_id")
        internal = self.updTable(Internal,
                                 columns=["job_id", "debt"],
                                 relColumns={"rBuilding":[["label"], ["building"]],
                                             "rStaffType":[["label"], ["staffType"]],
                                             "rSchool":[["label"], ["school"]],
                                             "rBookedBy":[["username", "first_name", "last_name", "school_id"],
                                                          ["bookedByUser", "bookedByFirstName", "bookedByLastName", "bookedBySchoolId"]]}).set_index("job_id")
        standardjobtype = self.updTable(StandardJobType,
                                 columns=["job_id", "equitment", "description", "number_items"],
                                 relColumns={"rAssignedUser": [["username", "first_name", "last_name"],
                                                               ["assignedUser", "assignedFirstName", "assignedLastName", "assignedSchoolId"]],
                                             "rLocation": [["label"], ["location"]]}).set_index("job_id")
        designjobtype = self.updTable(DesignJobType,
                                 columns=["job_id", "title", "specification"],
                                 relColumns={"rDesignUser": [["username", "first_name", "last_name", "school_id"],
                                                          ["designUser", "designFirstName", "designLastName", "designSchoolId"]],
                                             "rConstructorUser": [["username", "first_name", "last_name", "school_id"],
                                                                   ["constructorUser", "constructorFirstName", "constructorLastName", "constructorSchoolId"]]}).set_index("job_id")

        # Add a new column to associate job with table
        external["external"] = [True for x in external.index]
        internal["internal"] = [True for x in internal.index]
        standardjobtype["standardjobtype"] = [True for x in standardjobtype.index]
        designjobtype["designjobtype"] = [True for x in designjobtype.index]

        # Add all the columns from the tables associated with each job
        self.mJobs = pd.concat([self.mJobs, external, internal, standardjobtype, designjobtype], axis=1)
        # print(self.mJobs)
        # print(self.mJobs.columns)
        # print(self.mJobs.loc[1, :])
        return

    def updJobs(self):
        # Create a session
        session = orm.Session(bind=engine)
        # Note have not included visit,notes,email_collection,resolution from table
        # Create list of dataframes columns.
        data = [
            pd.read_sql('jobs', engine, columns=["job_number", "clone_from", "man_hours", "pph", "consumables", "completed_time", "created_at", "updated_at", "deleted_at"]),
            pd.DataFrame(self.getRelationCol(Jobs, "rJob_type", ["label"], name=["job_type"])),
            pd.DataFrame(self.getRelationCol(Jobs, "rHazards", ["label"], name=["hazards"])),
            pd.DataFrame(self.getRelationCol(Jobs, "rStatus", ["label"], name=["status"]))]
        # Create dataframe from columns
        self.mJobs = pd.concat(data, axis=1)
        print(self.mJobs.columns)
        # Close session
        session.close()
        return

    def updTable(self, table, **columns):
        # Create a session
        session = orm.Session(bind=engine)
        # Get the columns which are not related to other tables
        data = [pd.read_sql(table.__tablename__, engine, columns=columns.get("columns"))]
        # Iterate through each relationship column, and append to data the columns of associated table
        for key in columns.get("relColumns"):
            value = columns.get("relColumns")[key]
            data.append(pd.DataFrame(self.getRelationCol(table, key, value[0], name=value[1])))
        # Create dataframe from columns
        var = pd.concat(data, axis=1)
        # Close session
        session.close()
        return var


    '''
    # Returns a list of lists representing the columns of the associated table, using the relationship variable.
    # @param: "table": The table with the relationship variable.
    # @param: "relation": The string with name of the relationship variable.
    # @param: "columns": List of strings of column names wanted.
    # @param: "**options": "name": List of strings to replace column names from sql table according to order of "*columns".
    '''
    def getRelationCol(self, table, relation, columns, **options):
        session = orm.Session(bind=engine)
        query = session.query(table).all()
        table = {x: [] for x in columns}


        for row in query:
            linkTable = getattr(row, relation)
            for column in columns:
                if linkTable is not None:
                    table[column].append(getattr(linkTable, column))
                else:
                    table[column].append(None)

        session.close()

        if options.get("name") is None:
            return table
        else:
            for index, key in enumerate(list(table.keys())):
                table[options.get("name")[index]] = table.pop(key)
            return table

    mJobs = None